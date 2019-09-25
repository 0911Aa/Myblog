# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from repository import models
from utils.pagination import Pagination
from django.urls import reverse

from backend.auth.auth import check_login
from backend.forms.acticles import ArticleForm

@check_login
def index(request):
    # print(request.session.get("user_info"))
    return render(request,'backend_index.html')

@check_login
def article(request,*args,**kwargs):
    # print(kwargs)
    blog_id = request.session['user_info']['blog__bid']
    condition = {}
    for k, v in kwargs.items():
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id'] = blog_id
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p', 1), data_count)
    article_list = models.Article.objects.filter(**condition).order_by("-nid")[page.start:page.end]
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.article_type_choices)
    category_list = models.Category.objects.filter(blog_id=blog_id).values("nid","title")
    # print(category_list)
    kwargs["p"] = page.current_page
    return render(request,"backend_article.html",{
        "page_str":page_str,
        "type_list":type_list,
        "category_list":category_list,
        'arg_dict': kwargs,
        "article_list":article_list,
        "data_count":data_count,
    })


@check_login
def add_article(request):
    if request.method == "GET":
        form = ArticleForm(request)
        return render(request,"backend_add_article.html",{"form":form})