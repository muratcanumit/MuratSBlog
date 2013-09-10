from django.conf.urls import patterns, url
# from blogArticles.models import Post, Comment
from MuratSBlog import settings

urlpatterns = patterns(
    'blogArticles.views',
    url(r'^$', 'index', name="index"),
    url(r'^posts/(?P<post_id>\d+)/detail/$', 'detail', name="detail"),
    # url(r'^authors/(?P<author_username>\w+)/articles/$',
    # 'author', name="author"),
    # url(r'^(?P<comment_id>\d+)/comments/$',
    #     'show_comments', name='show_comments'),
)
