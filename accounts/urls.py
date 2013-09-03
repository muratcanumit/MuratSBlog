from django.conf.urls import include, patterns, url
from blogArticles.models import Post, Comment

urlpatterns = patterns(
    'accounts.views',
    url(r'^$', 'index', name="index"),    
)
