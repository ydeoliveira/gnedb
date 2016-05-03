from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change
from django.conf import settings

import os

from players.views import submit, search, single_search, nt_search

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', submit, name='submit'),
    url(r'^search/$', search, name='search'),
    url(r'^player/$', single_search, name='single_search'),
    url(r'^nt/$', nt_search, name='nt_search')


)

from django.contrib import databrowse
urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)$',
        'serve',
        dict(
            document_root = os.path.join(settings.PROJECT_PATH, 'media'),
            show_indexes = False
        )
    ),
    (r'^databrowse/(.*)', databrowse.site.root),
)