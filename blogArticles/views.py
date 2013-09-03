from blogArticles.models import Post, Comment
from accounts.models import UserProfile

from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

from django import template
from django.template.defaulttags import register
from django.template import RequestContext
from django.template import Context, loader

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from blogArticles.forms import PostAddFrom, CommentAddForm
from django.contrib import messages


# Shows the inde page of the blog with recent post's title, text and author
def index(request):
    latest_post_list = Post.objects.all().order_by('-created_on')[:10]
    return render(request, 'blogArticles/index.html',
                  {'latest_post_list': latest_post_list})


def author(request, author_id):
    return render(request, author_id)


# Shows on the site detailed Post, with comments and child comments
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


@login_required
def postAdding(request):
    if request.POST:
        form = PostAddFrom(request.POST)
        if form.is_valid():
            form.save(request.user)
            # image resize eklenecek
            # if request.FILES.get("post_image") is not None:
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PostAddFrom()

    return render(request, 'postadding.html', {'form': form})


# def commentAdding(request):


# inclusion tag for getting post's comments and their child comments
@register.inclusion_tag('blogArticles/print_childs.html')
def show_comments(parent, comment_list):
    parent = parent
    child_list = comment_list
    return {'parent': parent, 'child_list': child_list, }
