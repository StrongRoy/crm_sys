from django.shortcuts import render,HttpResponse
from .models import Questionnaire,Question,RadioQuestion
from django.db import transaction
from django.db.models import Count
# Create your views here.
from .forms import QuestionForm,RadioQuestionForm,QuestionnaireForm

def questionnaire_list(request):
    questionnaires = Questionnaire.objects.annotate(answer_count=Count('question__answer'))

    return render(request,'questionnaire_list.html',locals())

def questionnaire_done(request,*args,**kwargs):
    condition = kwargs.get('condition')
    questionnaire = None
    if len(kwargs)==2 and condition == 'edit':
        questionnaire = Questionnaire.objects.filter(pk=kwargs.get('pk')).first()
    if not questionnaire:
        questionnaire_form = QuestionnaireForm()
    else:
        questionnaire_form = QuestionnaireForm({'caption': questionnaire.caption,
                'group': questionnaire.group,})
    def inner(q):
        que_list = Question.objects.filter(questionnaire=q).annotate(option_count=Count('radioquestion'))
        if not que_list:
            yield {'form':QuestionForm(),'obj':None,'option_class':'hidden','options': [{'form': RadioQuestionForm(), 'obj': None, }]}
        else:
            for que in que_list:
                form = QuestionForm({'title': que.title,'q_type': que.q_type,})
                hidden ='' if que.q_type ==1 else 'hidden'
                def inner_loop(question):
                    option_list = RadioQuestion.objects.filter(question=question)
                    if not option_list:
                        yield {'form': RadioQuestionForm(), 'obj': None, }
                    else:
                        for option in option_list:
                            radio_form = RadioQuestionForm({'content': option.content, 'score': option.score})
                            yield {'form': radio_form, 'obj': option, }
                yield {'form': form, 'obj': que, 'option_class': hidden,'options':inner_loop(que)}

    return render(request,'questionnaire_done.html',{'form_list': inner(questionnaire),'questionnaire_form':questionnaire_form})




def questionnaire_save(request):
    user_id = 1
    if  request.method == 'POST':

        title_list = request.POST.getlist('title','')
        q_type_list = request.POST.getlist('q_type','')
        content_list = request.POST.getlist('content','')
        score_list = request.POST.getlist('score','')
        option_count_list = request.POST.getlist('option_count','')
        caption = request.POST.get('caption','')
        group = request.POST.get('group','')
        print(title_list,q_type_list,content_list,score_list,option_count_list,caption,group)
        # with transaction.atomic():
        #     questionnaire = Questionnaire.objects.create(caption=caption,user_id=user_id,group_id=group)
        #     for item in range(len(title_list)):
        #         title = title_list[item]
        #         q_type = q_type_list[item]
        #
        #         question = Question.objects.create(title=title,q_type=q_type,questionnaire=questionnaire)
        #         if q_type == '1':
        #             content = content_list[item]
        #             score = score_list[item]
        #             RadioQuestion.objects.create(content=content,score=score,question=question)

    return HttpResponse('ok')
