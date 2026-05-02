from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ContextInline(admin.StackedInline):
    model = Context
    extra = 1


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'read_time', 'author', 'category', 'published', 'important', 'created_at', 'get_cover')
    list_filter = ('category', 'tags', 'published')
    search_fields = ('title', 'intro')
    inlines = [ContextInline, CommentInline]

    def get_cover(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="80" height="45" style="object-fit:cover;border-radius:6px;" />',
                obj.cover.url
            )
        return "No Image"

    get_cover.short_description = "Muqova"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'email', 'name', 'content')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')