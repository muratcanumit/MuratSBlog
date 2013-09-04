from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.utils.translation import ugettext as _
from blogArticles.models import Post, Comment


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'post_image')
        labels = {'title': "Title",
                  'text': "Post Text",
                  'post_image': "Post Image"}
        help_texts = {
            'title': _('Title can be 150 characters at most'),
            'post_image': _('You can add an image to your post.'),
        }
        error_messages = {
            'title': {
                'max_length': _("This title is too long."),
            },
        }


class CommentAddForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
        labels = {'text': "Comment Text"}


class AnonCommentAddForm(CommentAddForm):
    anonymname = forms.CharField(required=True, label='anonymname',
                                 help_text=_('Give your anonym name.'))
    email = forms.EmailField(required=True, label='email',
                             help_text=_('You need to give email to comment.'))

    class Meta(CommentAddForm.Meta):
        model = Comment
        fields = ('anonymname', 'email', 'text')
