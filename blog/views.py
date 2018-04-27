# -*- coding:utf-8 -*-

import markdown
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.db.models import Q
from .models import Post, Category, Tag
from comments.forms import CommentForm

# # 主页
# def index(request):
#     # -为反向，不加是正向
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# # 详情
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 简化操作，打开详情即为阅读一次，自增一
#     post.increase_views()
#     # 使用markdown模块，防止转义前台页面要加'|safe'
#     post.body = markdown.markdown(
#         post.body, extensions=[
#             'markdown.extensions.extra',
#             # 语法高亮
#             'markdown.extensions.codehilite',
#             # 自动生成目录
#             'markdown.extensions.toc',
#         ]
#     )
#
#     # 同时获取post下的评论
#     comment_list = post.comment_set.all()
#     # 初始化form
#     form = CommentForm()
#
#     context = {
#         "post": post,
#         "form": form,
#         "comment_list": comment_list
#     }
#     return render(request, 'blog/detail.html', context=context)


# # 归档
# def archives(request, year, month):
#     post_list = Post.objects.filter(
#         create_time__year=year,
#         create_time__month=month
#     ).order_by('create_time')
#     return render(request, 'blog/index.html', context={"post_list": post_list})


# # 分类
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={"post_list": post_list})

# 关于
def aboutpage(request):
    return render(request, 'blog/about.html')


# 收藏
def collection(request):
    return render(request, 'blog/collection.html')


"""

以.下.为.主.要.类.视.图

"""


class IndexView(ListView):
    """
    index通用类视图，继承ListView
    """
    # 指定model为Post
    model = Post
    # 指定渲染的模板
    template_name = "blog/index.html"
    # 指定传递的变量名
    context_object_name = "post_list"
    # 指定分页器单页最大数据
    # 等价于 Paginator(list, pages_num)
    # 前台：
    # paginator：Paginator的实例。
    # page_obj：当前请求页面分页对象。
    # is_paginated：是否已分页（当分页后页面超过两页时才算已分页）
    paginate_by = 10

    # 以下为复杂分页，也就是先将所需数据生成，然后传递到模板中
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # 因为继承的是ListView，已有分页相关的三个变量
        paginator = context.get("paginator")
        page = context.get("page_obj")
        is_paginated = context.get("is_paginated")
        # 调用自己的分页方法
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # 将分页后的字典保存回context中
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        # 没有分页，返回空字典
        if not is_paginated:
            return {}
        # 分页条以中央位置为基准，需要记录左边有几个页码， 右边有几个页码
        left =[]
        right =[]
        # 第一页后是否需要...
        left_has_more = False
        # 最后一页前是否需要...
        right_has_more = False
        # 是否需要显示第一页的页码，当前左侧已有就不用显示
        first = False
        # 是否显示最后一页的页码，当前右侧已有就不用显示
        last = False
        # 用户选择的页码
        page_number = page.number
        # 总页数
        total_pages = paginator.num_pages
        # 分页条的列表
        page_range = paginator.page_range
        if page_range == 1:
            # 右侧显示当前页码之后的n个页码
            right = page_range[page_number:page_number+2]
            # 如果右侧最后一个页码比总页码倒数第二个还要少，则添加进...
            if right[-1] < total_pages-1:
                right_has_more =True
            # 如果右侧最后一个页码比总数小，说明右侧不含最后一个页码，需要显示
            if right[-1] <total_pages:
                last = True
        elif page_number == total_pages:
            # 如果用户选的是最后一页，右边就不需要数据，左边需要显示当前页码后连续n+1个页码
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0: page_number-1]
            # 如果left的第一个页码比n还大，则需要显示...
            if left[0] > 2:
                left_has_more = True
            # 如果left的第一个页码比1大，则left不包含第一页页码，需要显示
            if left[0] > 1:
                first =True
        else:
            # 用户随便点了一页
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0: page_number-1]
            right = page_range[page_number:page_number+2]
            # 最后一页之前的...
            if right[-1] < total_pages-1:
                right_has_more = True
            # 是否显示最后的页码
            if right[-1] < total_pages:
                last = True
            # 第一页之后的...
            if left[0] > 2:
                left_has_more = True
            # 是否显示第一页页码
            if left[0] > 1:
                first = True

        # 返回的结果
        data = {
            "left": left,
            "right": right,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "first": first,
            "last": last
        }
        return data


class CategoryView(IndexView):
    """
    category分类视图继承自index类视图
    """
    # 重写queryset方法，改变数据获取方式
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        # 再执行父类的filter方法
        # return super(CategoryView, self).get_queryset().filter(category=cate)
        # 同等
        return Post.objects.filter(category=cate)


class ArchivesView(IndexView):
    """
    archives归档视图继承自index类视图
    """
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super(ArchivesView, self).get_queryset().filter(
            create_time__year=year,
            create_time__month=month
        )


class PostDetailView(DetailView):
    """
    单条详情数据需要继承自DetailView类
    """
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        """
        重写get方法
        最后返回个HttpResponse
        当get被调用后才会有self.object，即为单条post
        """
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 阅读量+1
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        """
        重写get_object，需要对模板内容进行渲染
        :param queryset:
        :return:
        """
        post = super(PostDetailView, self).get_object(queryset=None)
        # 使用markdown模块，防止转义前台页面要加'|safe'
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            # 语法高亮
            'markdown.extensions.codehilite',
            # 自动生成目录锚点
            # 'markdown.extensions.toc',
            # 自定义锚点实例化，slugify方法处理中文
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        """
        重写get_context_data，不仅将post内容传到模板，还需要把form的实例传到前台
        :param kwargs:
        :return:
        """
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm
        comment_list = self.object.comment_set.all()
        context.update({
            "form": form,
            "comment_list": comment_list
        })
        return context


class TagView(IndexView):
    """
    标签视图类
    """
    def get_queryset(self):
        """
        重写get_queryset
        :return:
        """
        tag = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super(TagView, self).get_queryset().filter(tags=tag)


# 简单搜索方法
def search(request):
    """
    Q对象
    :param request:
    :return:
    """
    q = request.GET.get("q")
    error_msg = ""
    if not q:
        error_msg = "请输入关键词"
        return render(request, "blog/index.html", {"error_msg": error_msg})
    # __icontains包含，Q对象包装复杂查询，比如或'|'
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, "blog/index.html", {
        "error_msg": error_msg,
        "post_list": post_list
    })

