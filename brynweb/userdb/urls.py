from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^invite/$', views.invite, name='invite'),
    url(r'^accept-invite/(?P<uuid>[^/]+)$', views.accept_invite, name='accept-invite'),
    url(r'^validate-email/(?P<uuid>[^/]+)$', views.validate_email, name='validate-email'),
    url(r'^institutions/typeahead/$', views.institution_typeahead, name='institution_typeahead')
]
