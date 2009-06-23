from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/login_easy/', 'authmobile.views.login_easy', name='authmobile_login_easy'),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='auth_logout'),
    (r'^admin/(.*)', admin.site.root),

    url(r'', include('core.urls')),
)
