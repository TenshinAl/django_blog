#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/26 10:39
# @File    : search_indexes.py

from haystack import indexes
from .models import Post

"""
haystack创建索引，继承SearchIndex与Indexable
"""


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段document=True，use_template=True表示允许使用模板建立搜索
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


