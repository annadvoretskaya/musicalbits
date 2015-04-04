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
    url(r'^file/upload/ajax/$', 'file_upload_ajax', name='file_upload_ajax'),
    url(r'^$', 'home', name='home'),

)
