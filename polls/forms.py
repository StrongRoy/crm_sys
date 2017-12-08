# encoding:utf-8
# Author:Richie
# Date:12/4/2017
from django.forms import ModelForm,Select,TextInput,NumberInput
from .models import Question,RadioQuestion,Questionnaire


class QuestionnaireForm(ModelForm):
    class Meta:
        model = Questionnaire
        exclude = ['user']
        widgets={
            'caption':TextInput(attrs={'class': 'form-control', 'style':'width:50%;display: inline;','placeholder':'请输入问卷名称'}),
            'group':Select(attrs={'class': 'form-control selector','style':'width:50%;display: inline;'}),
        }

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','q_type']
        widgets = {
            'title': TextInput(attrs={'class':'form-control','style':'width:60%','placeholder':'请输入题目'}),
            'q_type': Select(attrs={'class': 'form-control selector','style':'width:50%;display: inline;'}),
        }

class RadioQuestionForm(ModelForm):
    class Meta:
        model = RadioQuestion
        fields = ['content','score']
        widgets = {
            'content': TextInput(attrs={'class': 'form-control', 'style':'width:30%;display: inline;'}),
            'score': NumberInput(attrs={'class': 'form-control','style':'width:30%;display: inline;', }),
        }


