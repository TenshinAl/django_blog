#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 14:32
# @File    : feeds.py

from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    """
    Rss订阅
    """
    # 标题
    title = "Matoi"
    # 链接
    link = "/"
    # 描述
    description = "来自木卫二"

    # 显示的内容
    def items(self):
        return Post.objects.all()

    # 显示的内容标题
    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    # 显示的内容描述
    def item_description(self, item):
        return item.body
