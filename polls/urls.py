from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^student/login/$',views.student_login,name='student_login'),
    url(r'^index/$',TemplateView.as_view(template_name='index.html')),
    url(r'^questionnaire/$', views.questionnaire_list),
    url(r'^questionnaire/(?P<condition>\w+)/$', views.questionnaire_done,name='que_add_save'),
    url(r'^questionnaire/(?P<condition>\w+)/(?P<pk>\d+)/$', views.questionnaire_done,name='que_delete_edit'),
    url(r'^student/evaluate/(?P<q_id>\d+)/(?P<group_id>\d+)/$',views.questionnaire_answer,name='questionnaire_answer'),


    # 会议室
    url(r'^room_predetermined/$',views.room_predetermined)
]
