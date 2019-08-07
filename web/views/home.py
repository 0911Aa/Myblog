# -*- coding: utf-8 -*-
from django.shortcuts import render
from repository import models
from django.urls import reverse
from utils.pagination import Pagination

def index(request,*args,**kwargs):
    print(request)
    print(kwargs)

    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        #在HTML中：{% url "index" article_type_id=1 %}             => all/1.html
        #在views中：reverse('index',kwargs={"article_type_id":1})  =>all/1.html
        base_url = reverse('index',kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    #分页查看，必要参数：当前页码、需要展示数据的总个数
    data_count = models.Article.objects.filter(**kwargs).count() #需要展示的总个数
    page_obj = Pagination(request.GET.get('p'), data_count)  #当前页码
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    type_list = models.Article.article_type_choices
    page_str = page_obj.page_str(base_url)

    return render(request,"index.html",
                  {
                      "type_list":type_list,
                      "article_type_id":article_type_id,
                      "article_list":article_list,
                      "page_str":page_str,
                  }
                  )

