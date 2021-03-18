from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

import os

from players.views import submit, search, single_search

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', submit, name='submit'),
    path('search/', search, name='search'),
    path('player/', single_search, name='single_search'),
    #path(r'^nt/$', nt_search, name='nt_search')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""from django.contrib import databrowse
urlpatterns += patterns('django.views.static',
    (r'^media/(?P<path>.*)$',
        'serve',
        dict(
            document_root = os.path.join(settings.PROJECT_PATH, 'media'),
            show_indexes = False
        )
    ),
    (r'^databrowse/(.*)', databrowse.site.root),
)"""
