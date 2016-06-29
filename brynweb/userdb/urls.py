from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url('^institutions/typeahead/$', views.institution_typeahead, name='institution_typeahead')
]
