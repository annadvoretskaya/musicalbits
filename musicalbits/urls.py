from django.conf.urls import patterns, include, url
from django.contrib import admin
#SOCIAL_AUTH_URL_NAMESPACE = 'social'
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.home', name='home'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),

    #url('', include('social.apps.django_app.urls', namespace='social')),
)
