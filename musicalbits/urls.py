from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),

)

urlpatterns += patterns('main.views',
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^signout/$', 'logout_user', name='logout_user'),
    url(r'^file/upload/$', 'file_upload', name='file_upload'),
    url(r'^file/delete/$', 'file_delete_ajax', name='file_delete_ajax'),
    url(r'^file/add/$', 'file_add_ajax', name='file_add_ajax'),
    url(r'^file/upload/ajax/$', 'file_upload_ajax', name='file_upload_ajax'),
    url(r'^$', 'home', name='home'),
    url(r'^search/$', 'search', name='search'),
    url(r'^music/$', 'music', name='music'),
    url(r'^rate/track/$', 'rate_track', name='rate_track'),
    url(r'^playlist/$', 'playlist', name='playlist'),
    url(r'^popular/$', 'playlist_popular', name='playlist_popular'),
    url(r'^new/$', 'new_track', name='new_track'),
    url(r'^playlist_edit_ajax/$', 'playlist_edit_ajax', name='playlist_edit_ajax'),
    url(r'^track_edit_ajax/$', 'track_edit_ajax', name='track_edit_ajax'),
    url(r'^playlist/(?P<id>\w+)/$', 'playlist_info', name='playlist_info'),
    url(r'^playlist/(?P<id>\w+)/edit/$', 'playlist_edit', name='playlist_edit'),
    url(r'^playlist/(?P<id>\w+)/like/$', 'playlist_like_ajax', name='playlist_like_ajax'),
    url(r'^playlist/(?P<id>\w+)/delete/$', 'playlist_delete', name='playlist_delete'),
    url(r'^sort_playlist/$', 'playlist_sort', name='playlist_sort'),

)
