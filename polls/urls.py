from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^index/$',TemplateView.as_view(template_name='index.html')),
    url(r'^questionnaire/$', views.questionnaire_list),
    url(r'questionnaire_save/$',views.questionnaire_save,name='questionnaire_save'),
    url(r'^questionnaire/(?P<condition>\w+)/$', views.questionnaire_done,name='que_add'),
    url(r'^questionnaire/(?P<condition>\w+)/(?P<pk>\d+)/$', views.questionnaire_done,name='que_delete_edit'),
]
