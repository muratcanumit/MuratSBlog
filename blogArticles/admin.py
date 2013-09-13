from blogArticles.models import Post, Comment
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import UserProfile


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


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['birth_date', 'gender',
                'is_verified', 'act_key', 'exp_key']}),
    ]

admin.site.register(UserProfile, UserProfileAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
