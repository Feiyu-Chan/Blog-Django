# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
from django.core import serializers
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    ordering = '-created_time'
    paginate_by = 8

    def get_context_data(self, **kwargs):

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []

        left_has_more = False
        right_has_more = False

        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                        'markdown.extensions.extra',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.toc',
                        'markdown.extensions.headerid',
                        'markdown.extensions.admonition'

                    ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/archive.html'
    context_object_name = 'post_list'
    ordering = '-created_time'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def about(request):
    return render(request, 'blog/about.html')


def archive(request):
    post_dict = {}
    data_list = Post.objects.dates('created_time', 'month', order='DESC')
    for date in data_list:
        post_list = Post.objects.filter(created_time__year=date.year,
                                    created_time__month=date.month
                                    ).order_by('-created_time')
        post_dict[date] = post_list
    return render(request, 'blog/archive.html', context={'post_list': post_dict})
