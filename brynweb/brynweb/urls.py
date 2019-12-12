from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^user/', include(('userdb.urls', 'user'), namespace='user')),
    url(r'^reports/', include(('reporting.urls', 'reports'), namespace='reports')),
    url(r'^discourse/', include(('discourse.urls', 'discourse'), namespace='discourse')),
    url(r'^admin/', admin.site.urls),
    url(r'', include(('home.urls', 'urls'), namespace='home')),
]
