# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
    """
    Django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)

    # ForeignKey、ManyToManyField : https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.PositiveIntegerField(default=0)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:75]
        super(Post, self).save(*args, **kwargs) # Call the real save() method
