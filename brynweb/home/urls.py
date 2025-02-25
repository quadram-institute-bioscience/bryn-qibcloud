from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^status$', views.status, name='status'),
    url(r'^region-select$', views.region_select, name='region-select'),
    url(r'^launch/(?P<teamid>\d+)$', views.launch, name='launch'),
    url(r'^launchcustom/(?P<teamid>\d+)$', views.launchcustom, name='launchcustom'),
    url(r'^start/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.start, name='start'),
    url(r'^stop/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.stop, name='stop'),
    url(r'^reboot/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.reboot, name='reboot'),
    url(r'^terminate/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.terminate, name='terminate'),
    url(r'^unshelve/(?P<teamid>\d+)/(?P<uuid>[^/]+)$', views.unshelve, name='unshelve'),
    url(r'^get_instances_table', views.get_instances_table, name='get_instances_table'),
    url(r'^$', views.home, name='home'),
]
