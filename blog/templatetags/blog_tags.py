# -*- coding: utf-8 -*-
from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_hot_posts(num=5):
    return Post.objects.all().order_by('-views')[:num]


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)
