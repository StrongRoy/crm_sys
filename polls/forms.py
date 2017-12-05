# encoding:utf-8
# Author:Richie
# Date:12/4/2017

from django.forms import ModelForm,Textarea,Select
from .models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'title': Textarea(attrs={'cols': 1, 'rows': 1,'class':'form-control','placeholder':'请输入题目'}),

            'q_type': Select(attrs={'class': 'form-control'}),
        }

