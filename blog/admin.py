# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_time', 'updated_time']

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
