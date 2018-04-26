#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 15:30
# @File    : forms.py

from django import forms
from .models import Comment


# 评论的form，对应数据库使用ModelForm比较好
class CommentForm(forms.ModelForm):
    # 内部类
    class Meta:
        # 指定模型
        model = Comment
        # 指定字段
        fields = ['name', 'email', 'url', 'text']


