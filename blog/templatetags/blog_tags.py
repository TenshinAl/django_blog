#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 10:46
# @File    : blog_tags.py

"""
自定义标签
"""

from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count


# 标签注册器
register = template.Library()


# 根据创建时间反向排序，默认为前五篇文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


# 归档
@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


# 分类
@register.simple_tag
def get_categories():
    # return Category.objects.all()
    # 聚合统计：计算分类下的文章数，其接受的参数为需要计数的模型的名称，并且只要num_posts数量大于0的值
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# tag标签
@register.simple_tag
def get_tags():
    # 同分类
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

