from django.conf.urls import patterns, url
from blogArticles.models import Post, Comment


urlpatterns = patterns(
    'blogArticles.views',
    url(r'^$', 'index', name="index"),
    url(r'^add-post/$', 'postAdd', name="addpost"),
    url(r'^posts/(?P<post_id>\d+)/detail/$', 'detail', name="detail"),
    # url(r'^authors/(?P<author_username>\w+)/articles/$', 'author', name="author"),
    # url(r'^(?P<comment_id>\d+)/comments/$',
    #     'show_comments', name='show_comments'),
)
