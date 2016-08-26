from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^user/', include('userdb.urls', namespace='user')),
    url(r'^reports/', include('reporting.urls', namespace='reports')),
    url(r'^discourse/', include('discourse.urls', namespace='discourse')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('home.urls', namespace='home')),
]
