# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


# Create your models here.


# 用装饰器兼容py2
@python_2_unicode_compatible
class Category(models.Model):
    """
    模型必须继承models.Model类
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    """
    文章内容相关
    """
    title = models.CharField(max_length=70)
    # 正文内容使用textfield
    body = models.TextField()
    # 时间使用Datetimefield
    create_time = models.DateField()
    modified_time = models.DateField()
    # 开头摘要，可为空
    excerpt = models.CharField(max_length=200, blank=True)
    """
    分类标签相关
    """
    # 分类类型为主键,on_delete=models.CASCADE
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 一篇文章对应多个标签，一个标签也对应多个文章，当然也能为空
    tags = models.ManyToManyField(Tag, blank=True)
    """
    文章作者，django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程
    on_delete=models.CASCADE
    也应该是个主键，参数是由user那边的传过来的
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 阅读量，应该是个自增量，默认0
    views = models.PositiveIntegerField(default=0)

    # 调用此方法实现自增，数据库更新此字段
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 重写get_absolute_url，需要reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 自动保存摘要，重写个save
    def save(self, *args, **kwargs):
        # 如果内容摘要为空
        if not self.excerpt:
            # 设置一个md配置
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 将md内容转换为html
            # django下的工具类中的strip_tags方法可以去除html的标签，顺便只取前54个字符
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 处理完成后使用父类中的save进行真正保存
        super(Post, self).save(*args, **kwargs)

    # 内部类，定义默认排序方式
    class Meta:
        ordering = ['-create_time', 'title']
