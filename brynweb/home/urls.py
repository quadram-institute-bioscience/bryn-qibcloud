from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.loginpage, name='login'),
    url(r'^logout$', views.logoutview, name='logout'),
    url(r'^launch/(?P<teamid>\d+)$', views.launch, name='launch'),
    url(r'^launchcustom/(?P<teamid>\d+)$', views.launchcustom, name='launchcustom'),
    url(r'^start/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.start, name='start'),
    url(r'^stop/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.stop, name='stop'),
    url(r'^reboot/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.reboot, name='reboot'),
    url(r'^terminate/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.terminate, name='terminate'),
    url(r'^get_instances_table', views.get_instances_table, name='get_instances_table'),
    url(r'^$', views.home, name='home'),
]
