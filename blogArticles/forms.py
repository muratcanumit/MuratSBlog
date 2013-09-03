from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.forms import ModelForm


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'post_image')
        labels = {'title': "Title",
                  'text': "Post Text",
                  'post_image': "Post Image"}
        help_texts = {
            'title': 'Title can be 150 characters at most',
            'post_image': 'You can add an image to your post.',
        }
        error_messages = {
            'title': {
                'max_length': "This title is too long.",
            },
        }


class CommentAddForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text')
        labels = {'text': "Comment Text"}
        widgets = {'text': forms.TextArea(attrs={'cols': 100, 'rows': 25})}
