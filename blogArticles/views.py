from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaulttags import register
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# from blogArticles.tasks import resizePostImage
from blogArticles.models import Post, Comment
from blogArticles.forms import PostAddForm
#, CommentAddForm, AnonCommentAddForm

# from django.core.paginator import Paginator, InvalidPage, EmptyPage


# Shows the index page of the blog with recent post's title, text and author

def index(request):
    latest_post_list = Post.objects.all().order_by('-created_on')[:20]
    return render(request, 'blogArticles/index.html',
                  {'latest_post_list': latest_post_list})


def all_articles(request):
    all_articles = Post.objects.all().order_by('-created_on')
    return render(request, 'blogArticles/all_articles.html',
                  {'all_articles': all_articles})


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


# inclusion tag for getting post's comments and their child comments
@register.inclusion_tag('blogArticles/print_childs.html')
def show_comments(parent, comment_list):
    parent = parent
    child_list = comment_list
    return {'parent': parent, 'child_list': child_list, }


@login_required
def postAdd(request):
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('index'))
        else:
            messages.error(request, _('Post was not Added !'))
    else:
        form = PostAddForm()
    return render(request, 'blogArticles/postadd.html', {'form': form})


# def commentAdd(request, content_type, entity_id, object_id):
#     if content_type == 'post':
#         parent = get_object_or_404(Post.objects.select_related(), pk=id)
#         entity_id = parent.id
#     elif content_type == 'comment':
#         parent = get_object_or_404(Comment.objects.select_related('object_id'), pk=id)
#         entity = parent.entity_id
#     else:
#         return HttpResponseRedirect(reverse('detail'))

#     if request.method == 'POST':
#         if request.user.is_authenticated():
#             form = CommentAddForm(request.POST)
#         else:
#             form = AnonCommentAddForm

#         if form.is_valid():
#             form.save(request.user, parent, entity)
#             if request.user.is_authenticated():
#                 messages.success(request, _('Comment added!'))
#             else:
#                 messages.success(request, _('Verify your comment with key.'))
#                 return HttpResponseRedirect(reverse('detail'))
#         else:
#             messages.error(_('Comment could not added.'))
#             return HttpResponseRedirect(reverse('detail'))
#     else:
#         messages.error(request, _('An error occured.'))
#         if request.user.is_authenticated():
#             form = CommentAddForm()
#         else:
#             form = AnonCommentAddForm

#     return render(request, 'commentadd.html', {'form': form})


def about(request):
    return render(request, 'blogArticles/about.html')
