from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'userdb/password_reset_form.html',
         'email_template_name': 'userdb/email/password_reset_email.txt',
         'html_email_template_name': 'userdb/email/password_reset_email.html',
         'subject_template_name': 'userdb/email/password_reset_subject.txt',
         'post_reset_redirect': 'user:password_reset_done'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'userdb/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'userdb/password_reset_confirm.html',
         'post_reset_redirect': 'user:password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'userdb/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^invite/$', views.invite, name='invite'),
    url(r'^accept-invite/(?P<uuid>[^/]+)$', views.accept_invite,
        name='accept-invite'),
    url(r'^validate-email/(?P<uuid>[^/]+)$', views.validate_email,
        name='validate-email'),
    url(r'^institutions/typeahead/$', views.institution_typeahead,
        name='institution_typeahead')
]
