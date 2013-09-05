from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from MuratSBlog import settings
from django.conf.urls.static import static

handler404 = 'blogArticles.errorviews.errorView404'
handler500 = 'blogArticles.errorviews.errorView500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^', include('blogArticles.urls')),
    url(r'^', include('accounts.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
