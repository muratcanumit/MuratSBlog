from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blogArticles.urls')),
    url(r'^', include('accounts.urls')),
)

if settings.DEBUG is True:
    urlpatterns = patterns(
        '',
        url(r'^uploadedmedia/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    ) + urlpatterns

urlpatterns += staticfiles_urlpatterns()

handler404 = 'MuratSBlog.views.handler404'
handler500 = 'MuratSBlog.views.handler500'
