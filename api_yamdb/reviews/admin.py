from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_DISPLAY

from .models import Categories, Comment, Genre, Review, Title


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    list_editable = ('category',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'pub_date', 'score', 'text',)
    list_editable = ('text', 'score',)
    list_filter = ('title', 'author',)
    search_fields = ('title', 'author',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'review', 'author', 'text', 'pub_date',)
    list_editable = ('text',)
    list_filter = ('pub_date', 'author', 'title', 'review',)
    search_fields = ('author', 'title', 'review', 'text',)
    empty_value_display = EMPTY_VALUE_DISPLAY
