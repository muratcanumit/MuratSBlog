from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.generic import (GenericForeignKey,
                                                 GenericRelation)


class Post(models.Model):
    title = models.CharField(max_length=150)
    text = RichTextField()
    author = models.ForeignKey(User)
    post_image = models.ImageField(blank=True, upload_to="postimages")
    created_on = models.DateTimeField(auto_now_add=True)
    # to get sub comments from the parent
    comments = GenericRelation('Comment')

    def __unicode__(self):
        return u"%s" % self.title

    #to order comments by date reverse
    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User)
    entity = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)
    # GenericForeignKey Usage
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    # to get sub comments from the parent
    comments = GenericRelation('Comment')

    def __unicode__(self):
        return u"%s" % self.text

    #to order comments by date reverse
    class Meta:
        ordering = ['created_on']
