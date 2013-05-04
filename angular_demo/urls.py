from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^hello$', TemplateView.as_view(template_name='angular_demo/01_hello.html')),
    url(r'^todo$', TemplateView.as_view(template_name='angular_demo/02_todo.html')),
)
