from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^questionnaire_list/$', views.questionnaire_list, name='questionnaire_list'),
    url(r'^questionnaire_add/$', views.questionnaire_add, name='questionnaire_add'),
    url(r'^questionnaire_save/$', views.questionnaire_save, name='questionnaire_save'),

]
