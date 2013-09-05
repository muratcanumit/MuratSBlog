from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

handler404 = 'blogArticles.errorviews.errorView404'
handler500 = 'blogArticles.errorviews.errorView500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^', include('blogArticles.urls')),
    url(r'^', include('accounts.urls')),
)
