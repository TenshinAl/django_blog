# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .forms import CommentForm


def post_comment(request, post_pk):
    """
    通过post的id获取关联的评论信息
    :param request:
    :param post_pk:
    :return:
    """
    # 存在post时获取，没有就404
    post = get_object_or_404(Post, pk=post_pk)

    # post请求
    if request.method == 'POST':
        # 构造表单实例
        form = CommentForm(request.POST)

        # 使用自带的数据检查方法
        if form.is_valid():
            # 先保存进对象
            comment = form.save(commit=False)
            # 关联评论与post
            comment.post = post
            # 然后保存
            comment.save()

        # 出现了数据填写错误或者是其他情况
        else:
            # post.comment_set.all()和post.objects.all()类似，因为存在了外键，所以能反向查出post下的comment
            comment_list = post.comment_set.all()
            context = {
                "post": post,
                "form": form,
                "comment_list": comment_list
            }
            # 使用现有内容进行返回
            return render(request, 'blog/detail.html', context=context)

    # 重定向回原post，redirect接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
    return redirect(post)


