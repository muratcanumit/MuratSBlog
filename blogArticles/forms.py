from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.utils.translation import ugettext as _
from blogArticles.models import Post, Comment


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
        labels = {'title': _('Title'),
                  'text': _('Post Text'),
                  'post_image': _('Post Image')}
        help_texts = {
            'title': _('Title can be 150 characters at most'),
            'post_image': _('You can add an image to your post.'),
        }
        error_messages = {
            'title': {
                'max_length': _('This title is too long.'),
            },
        }


# class CommentAddForm(forms.ModelForm):

#     class Meta:
#         model = Comment
#         fields = ('text')
#         labels = {'text': "Comment Text"}

#     def save(self, request, parent, entity):
#         comment = Comment(
#             text=self.cleaned_data['text'],
#             author=request.user,
#             entity=entity,
#             content_type=ContentType.objects.get_for_model(parent),
#             object_id=parent.id,
#             is_verified=True,
#             email=request.user.email)
#         comment.save()


# class AnonCommentAddForm(CommentAddForm):
#     email = forms.EmailField(required=True, label='email',
#                            help_text=_('You need to give email to comment.'))

#     class Meta(CommentAddForm.Meta):
#         model = Comment
#         fields = ('email', 'text')

#     def save(self, request, parent, entity):
#         comment = Comment(
#             text=self.cleaned_data['text'],
#             author=request.user,
#             entity=entity,
#             content_type=ContentType.objects.get_for_model(parent),
#             object_id=parent.id,
#             is_verified=False,
#             email=request.user.email)
#         comment.save()
