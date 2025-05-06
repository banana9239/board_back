from django.contrib import admin
from .models import Post, PostComment, CommenReply, Browsing, PostLike

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'board', 'sortation', 'created_at','is_deleted']
    search_fields = ['title', 'author', 'board', 'sortation', 'is_deleted']
    list_filter = ['author', 'board', 'sortation', 'is_deleted', 'created_at']
    fieldsets = (
        (
            "Post",
            {
                "fields": (
                    "title",
                    "content",
                    "author",
                    "board",
                    "sortation",
                    "is_deleted",
                ),
                "classes": ("wide",),
            },
        ),
    )

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'post', 'created_at','is_deleted']
    search_fields = ['content', 'author', 'post', 'is_deleted']
    list_filter = ['author', 'post', 'is_deleted', 'created_at']
    fieldsets = (
        (
            "PostComment",
            {
                "fields": (
                    "content",
                    "author",
                    "post",
                    "is_deleted",
                ),
                "classes": ("wide",),
            },
        ),
    )

@admin.register(CommenReply)
class CommenReplyAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'comment', 'created_at','is_deleted']
    search_fields = ['content', 'author', 'comment', 'is_deleted']
    list_filter = ['author', 'comment', 'is_deleted', 'created_at']
    fieldsets = (
        (
            "CommenReply",
            {
                "fields": (
                    "content",
                    "author",
                    "comment",
                    "is_deleted",
                ),
                "classes": ("wide",),
            },
        ),
    )

@admin.register(Browsing)
class BrowsingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at']
    search_fields = ['post', 'user']
    list_filter = ['post', 'user', 'created_at']
    fieldsets = (
        (
            "Browsing",
            {
                "fields": (
                    "post",
                    "user",
                ),
                "classes": ("wide",),
            },
        ),
    )

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    search_fields = ['post', 'user']
    list_filter = ['post', 'user', 'created_at']
    fieldsets = (
        (
            "PostLike",
            {
                "fields": (
                    "post",
                    "user",
                ),
                "classes": ("wide",),
            },
        ),
    )