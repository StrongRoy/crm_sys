import json
from django.shortcuts import render, HttpResponse, redirect
from .models import Questionnaire, Question, RadioQuestion, Student, Answer,Room,MeetingRoom
from django.db import transaction
from django.core.exceptions import ValidationError
# Create your views here.
from .forms import QuestionForm, RadioQuestionForm, QuestionnaireForm


def student_login(request):
    obj = Student.objects.filter(name='兴平', password='123').first()
    request.session['student_info'] = {'id': obj.id, 'name': obj.name}
    return HttpResponse('登录成功')


def questionnaire_list(request):
    questionnaires = Questionnaire.objects.all()
    for i in questionnaires:
        count = Answer.objects.filter(question__questionnaire=i).values('student_id').distinct().count()
        i.count = count

    return render(request, 'questionnaire_list.html', locals())


def questionnaire_done(request, **kwargs):
    user_id = 1
    condition = kwargs.get('condition')
    pk = kwargs.get('pk')
    if request.method == 'GET':
        if condition == 'edit':
            questionnaire = Questionnaire.objects.filter(pk=pk).first()
            if questionnaire:
                questionnaire_form = QuestionnaireForm({'caption': questionnaire.caption,
                                                        'group': questionnaire.group, })
            else:
                return redirect('/questionnaire/add/')
        elif condition == 'delete':
            Questionnaire.objects.filter(pk=pk, user_id=user_id).delete()
            return redirect('/questionnaire/')
        elif condition == 'add':
            questionnaire = None
            questionnaire_form = QuestionnaireForm()
        else:
            return render(request, 'notFound.html')

        def inner(_questionnaire):
            que_list = Question.objects.filter(questionnaire=_questionnaire)
            if not que_list:
                yield {'form': QuestionForm(), 'obj': None, 'option_class': 'hidden', 'options': None}
            else:
                for que in que_list:
                    form = QuestionForm({'title': que.title, 'q_type': que.q_type, })
                    hidden = '' if que.q_type == 1 else 'hidden'

                    def inner_loop(_question):
                        option_list = RadioQuestion.objects.filter(question=_question)
                        for _option in option_list:
                            radio_form = RadioQuestionForm({'content': _option.content, 'score': _option.score})
                            yield {'form': radio_form, 'obj': _option, }

                    yield {'form': form, 'obj': que, 'option_class': hidden, 'options': inner_loop(que)}

        return render(request, 'questionnaire_done.html',
                      {'form_list': inner(questionnaire), 'questionnaire_form': questionnaire_form})
    elif request.method == 'POST' and request.is_ajax() and condition == 'save':

        # 模拟用户

        question_data_list = json.loads(request.POST.get('question_data_list', ''))
        caption = request.POST.get('caption', '')
        group = request.POST.get('group', '')
        try:
            with transaction.atomic():
                # 问卷更新或创建
                query_questionnaire_ret = Questionnaire.objects.update_or_create(caption=caption, group_id=group,
                                                                                 user_id=user_id)
                done = '新增' if query_questionnaire_ret[1] else '更新'

                db_question_list = Question.objects.filter(questionnaire=query_questionnaire_ret[0])

                # 处理需要删除的问题

                # 用户提交的需修改的问题id列表
                post_question_id_list = [item.get('q_id') for item in question_data_list if item.get('q_id')]
                # 数据库已经存在的问题id列表
                db_question_id_list = [item.id for item in db_question_list]

                # 数据库中那些事需要删除的id列表
                post_question_id_list = set(db_question_id_list).difference(post_question_id_list)
                # 删除需要删除的所有问题
                Question.objects.filter(id__in=post_question_id_list).delete()

                for question in question_data_list:
                    q_id = question.get('q_id') if question.get('q_id') else 0

                    title = question.get('title', '')
                    q_type = int(question.get('q_type', 0))

                    # 处理需要删除的选项

                    # 找到问题中需要删除的选项
                    db_option_list = RadioQuestion.objects.filter(question_id=q_id)
                    # 用户提交的需要修改的选项id列表
                    if 'o_id' in question:
                        post_option_id_list = [item.get('o_id') for item in question if item.get('o_id')]
                    else:
                        post_option_id_list = []
                    # 找到数据控中已存在的选项id列表
                    db_option_id_list = [item.id for item in db_option_list]
                    # 数据库中那些事需要删除选项id列表
                    del_option_id_list = set(db_option_id_list).difference(post_option_id_list)
                    RadioQuestion.objects.filter(id__in=del_option_id_list).delete()

                    # 处理问题的添加更新和选项的添加更新
                    query_question_ret = Question.objects.update_or_create(title=title, q_type=q_type,
                                                                           questionnaire=query_questionnaire_ret[0])
                    # 处理选项相关的更新和添加
                    for option in question.get('options', ''):
                        content = option.get('content', '')
                        score = int(option.get('score', 0))
                        RadioQuestion.objects.update_or_create(content=content, score=score,
                                                               question=query_question_ret[0])

            result = {"status": "success", 'done': done}

        except Exception as e:
            result = {"status": "fail", 'message': str(e)}

        return HttpResponse(json.dumps(result))
    return HttpResponse("error")


def func(val):
    if len(val) < 15:
        raise ValidationError('你太短了')


def questionnaire_answer(request, **kwargs):
    group_id = kwargs.get('group_id')
    q_id = kwargs.get('q_id')

    student_id = request.session.get('student_info').get('id')

    # 1. 当前登录用户是否是要评论的班级的学生
    if not Student.objects.filter(id=student_id, group_id=group_id).exists():
        return HttpResponse('你只能评论自己班级的问卷，是不是想转班？')
    # 2. 你是否已经提交过当前问卷答案
    if Answer.objects.filter(student_id=student_id, question__questionnaire_id=q_id).exists():
        return HttpResponse('你已经参与过调查，无法再次进行')

    from django import forms
    # 找到问卷的问题列表
    question_list = Question.objects.filter(questionnaire_id=q_id)
    field_dict = {}
    for question in question_list:
        if question.q_type == 1:
            # 单选
            field_dict['option_id_%s' % question.id] = forms.ChoiceField(
                label=question.title,
                error_messages={'required': '必填'},
                choices=RadioQuestion.objects.filter(question=question).values_list('id', 'content'),
                widget=forms.RadioSelect
            )

        elif question.q_type == 2:
            # 建议
            field_dict['content_%s' % question.id] = forms.CharField(
                label=question.title,
                error_messages={'required': '必选'},
                widget=forms.Textarea,
                validators=[func,]
            )

        elif question.q_type == 3:
            # 打分
            field_dict['score_%s' % question.id] = forms.ChoiceField(
                label=question.title,
                error_messages={'required': '必填'},
                choices=[(i, str(i) + '分') for i in range(1, 11)],
                widget=forms.RadioSelect
            )

    answer_form = type("AnswerForm", (forms.Form,), field_dict)

    if request.method == 'GET':
        form = answer_form()
        return render(request, 'questionnaire_answer.html', {'form': form})
    elif request.method == 'POST':
        form = answer_form(request.POST)
        if form.is_valid():
            obj_list = []
            for key,val in form.cleaned_data.items():
                k,q_id = key.rsplit('_',1)
                answer_dict = {'student_id': student_id, 'question_id': q_id, k: val}
                print(answer_dict)
                obj_list.append(Answer(**answer_dict))
            print([i for i in obj_list])
            Answer.objects.bulk_create(obj_list)
        return render(request, 'questionnaire_answer.html', {'form': form})
    return HttpResponse('error')

def room_predetermined(request):
    if request.method == 'GET':
       room_list =  Room.objects.all()
       return render(request,'predetermined.html',locals())

    elif request.method  == 'POST':
        pass

    return HttpResponse('error')
