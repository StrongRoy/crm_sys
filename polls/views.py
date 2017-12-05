from django.shortcuts import render,HttpResponse
from .models import Questionnaire,Question
# Create your views here.
from .forms import QuestionForm

def questionnaire_list(request):
    questionnaires = Questionnaire.objects.all()
    return render(request,'questionnaire_list.html',locals())


def questionnaire_add(request):

    question_form = QuestionForm()
    return render(request,'questionnaire_add.html',locals())


def questionnaire_save(request):
    return HttpResponse('ok')
