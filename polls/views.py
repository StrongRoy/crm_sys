import json
from django.shortcuts import render, HttpResponse,redirect
from .models import Questionnaire, Question, RadioQuestion
from django.db import transaction
from django.db.models import Count
# Create your views here.
from .forms import QuestionForm, RadioQuestionForm, QuestionnaireForm


def questionnaire_list(request):
    questionnaires = Questionnaire.objects.annotate(answer_count=Count('question__answer'))

    return render(request, 'questionnaire_list.html', locals())


def questionnaire_done(request, *args, **kwargs):
    if request.method == 'GET':
        condition = kwargs.get('condition')

        if condition == 'edit':
            questionnaire = Questionnaire.objects.filter(pk=kwargs.get('pk')).first()
            if questionnaire:
                questionnaire_form = QuestionnaireForm({'caption': questionnaire.caption,
                                                        'group': questionnaire.group, })
            else:
                return redirect('/questionnaire/add/')
        elif condition == 'delete':
            # 找到问卷 删除所有与之关联的数据
            Questionnaire.objects.filter(pk=kwargs.get('pk')).delete()
            return redirect('/questionnaire/')
        else:
            questionnaire = 0
            questionnaire_form = QuestionnaireForm()

        def inner(q):
            que_list = Question.objects.filter(questionnaire=q)
            if not que_list:
                yield {'form': QuestionForm(), 'obj': None, 'option_class': 'hidden', 'options': None}
            else:

                for que in que_list:
                    form = QuestionForm({'title': que.title, 'q_type': que.q_type, })
                    hidden = '' if que.q_type == 1 else 'hidden'

                    def inner_loop(question):
                        option_list = RadioQuestion.objects.filter(question=question)
                        for option in option_list:
                            radio_form = RadioQuestionForm({'content': option.content, 'score': option.score})
                            yield {'form': radio_form, 'obj': option, }

                    yield {'form': form, 'obj': que, 'option_class': hidden, 'options': inner_loop(que)}

        return render(request, 'questionnaire_done.html',
                      {'form_list': inner(questionnaire), 'questionnaire_form': questionnaire_form})
    else:
        return HttpResponse('error')


def questionnaire_save(request):
    user_id = 1
    if request.is_ajax() and request.method == 'POST':
        question_data_list = json.loads(request.POST.get('question_data_list', ''))
        caption = request.POST.get('caption', '')
        group = request.POST.get('group', '')
        with transaction.atomic():
            # 问卷保存
            query_questionnaire_obj = Questionnaire.objects.update_or_create(caption=caption, group_id=group,
                                                                             user_id=user_id)
            for question in question_data_list:
                title = question.get('title', '')
                q_type = int(question.get('q_type', 0))
                query_que_obj = Question.objects.update_or_create(title=title, q_type=q_type)
                query_que_obj[0].questionnaire.add(query_questionnaire_obj[0])
                for option in question.get('options', ''):
                    content = option.get('content', '')
                    score = int(option.get('score', 0))
                    query_rad_obj = RadioQuestion.objects.update_or_create(content=content, score=score)
                    query_rad_obj[0].question.add(query_que_obj[0])
        result = {"status": "success"}
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")
