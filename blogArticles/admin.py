from blogArticles.models import Post, Comment
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'text', 'author']})
    ]

    list_display = ('title', 'text', 'author', 'created_on')
    list_filter = ['created_on']
    date_hierarchy = 'created_on'

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['text', 'author', 'entity',
                'content_type', 'object_id']}),
    ]

    list_display = ('text', 'author', 'created_on')
    list_filter = ['created_on']
    date_hierarchy = 'created_on'

admin.site.register(Comment, CommentAdmin)
