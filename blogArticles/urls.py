from django.conf.urls import patterns, url
from blogArticles.models import Post, Comment

urlpatterns = patterns(
    'blogArticles.views',
    url(r'^$', 'index', name="index"),
    url(r'^posts/(?P<post_id>\d+)/detail/$', 'detail', name="detail"),
    url(r'^postadd/$', 'postAdd', name="postadd"),
    url(r'^all_articles/$', 'all_articles', name="all_articles"),
    url(r'^about/$', 'about', name="about"),
)
