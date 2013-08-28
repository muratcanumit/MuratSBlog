from django.template import Context, loader
from django.shortcuts import get_object_or_404, render
from blogArticles.models import Post, Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django import template
from django.template.defaulttags import register
from django.contrib.contenttypes.models import ContentType


def index(request):
    latest_post_list = Post.objects.all().order_by('-created_on')[:10]
    return render(request, 'blogArticles/index.html',
                  {'latest_post_list': latest_post_list})


def author(request, author_id):
    return render(request, author_id)


def detail(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    ct_post = ContentType.objects.get_for_model(Post)
    post_comments = Comment.objects.filter(entity=post_id).order_by(
        'created_on').filter(content_type=ct_post)

    ct_comment = ContentType.objects.get_for_model(Comment)
    comment_list = Comment.objects.filter(entity=post_id).order_by(
        'created_on').filter(content_type=ct_comment)
    # return redirect(request, reverse('urls_name'))
    return render(request, 'blogArticles/detail.html',
                  {'post': p, 'comment_list': comment_list,
                   'post_comment_list': post_comments})


@register.inclusion_tag('blogArticles/print_childs.html')
def show_comments(parent, comment_list):
    parent = parent
    child_list = comment_list
    return {'parent': parent, 'child_list': child_list, }
