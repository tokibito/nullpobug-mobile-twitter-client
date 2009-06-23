from django.conf.urls.defaults import *

urlpatterns = patterns('core.views',
    url(r'^$', 'index',  name='site_index'),
    url(r'^post_message$', 'post_message',  name='core_post_message'),
    url(r'^retweet/(?P<message_id>\d+)$', 'retweet_message',  name='core_retweet_message'),
    url(r'^fetch_friends_timeline/$', 'fetch_friends_timeline',  name='core_fetch_friends_timeline'),

    url(r'^config$', 'config',  name='core_config'),
    url(r'^config_login_easy$', 'config_login_easy',  name='core_config_login_easy'),
)
