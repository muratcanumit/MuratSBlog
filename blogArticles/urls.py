from django.conf.urls import include, patterns, url
from blogArticles.models import Post, Comment

urlpatterns = patterns(
    'blogArticles.views',
    url(r'^$', 'index', name="index"),
    url(r'^(?P<post_id>\d+)/detail/$', 'detail', name="detail"),
    url(r'^(?P<author_id>\d+)/author/$', 'author', name="author"),
    url(r'^(?P<comment_id>\d+)/comments/$',
        'show_comments', name='show_comments'),
)
