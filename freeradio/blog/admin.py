from django.contrib import admin
from django import forms
from .models import *
from .forms import *


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_displaly = ('name', 'user')
    form = BloggerForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class PostForm(forms.ModelForm):
    class Meta:
        widgets = {
            'body': RedactorWidget
        }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    search_fields = ('title', 'body')
    prepopulated_fields = {
        'slug': ('title',)
    }

    filter_horizontal = ('categories',)
    form = PostForm

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'body',
                    'featured_image',
                    'categories',
                    'tags'
                )
            }
        ),
        (
            None,
            {
                'fields': (
                    'slug',
                    'author',
                    'blogger',
                    'published',
                    'excerpt'
                )
            }
        )
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        if db_field.name == 'author':
            field.initial = request.user

        return field
