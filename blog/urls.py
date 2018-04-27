#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 15:46
# @File    : urls.py

from django.conf.urls import url
from blog.feeds import AllPostsRssFeed
from . import views

app_name = 'blog'
urlpatterns = [
    # django2.0后使用path，不过用1.0的项目比较多
    # path('post/<int:pk>/', views.detail, name='detail'),
    # as_view将类视图转换为函数
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9])/$', views.TagView.as_view(), name="tag"),
    url(r'^about/$', views.aboutpage, name='about'),
    url(r'collection/$', views.collection, name='collection'),
    # 简单搜索
    # url(r'^search/$', views.search, name="search"),
    # RSS订阅
    url(r'^all/rss/$', AllPostsRssFeed(), name="rss"),
]

