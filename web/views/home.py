# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from repository import models
from django.urls import reverse
from utils.pagination import Pagination


#主页
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
    #为了显示最新内容在最上面，需要加上order_by,参数加-就是倒序（desc），不加就是顺序（asc）
    article_list = models.Article.objects.filter(**kwargs).order_by('nid')[page_obj.start:page_obj.end]
    type_list = models.Article.article_type_choices
    #page_str就是分页工具最后生成的那一排a标签，要传到前端去显示
    page_str = page_obj.page_str(base_url)

    return render(request,"index.html",
                  {
                      "type_list":type_list,
                      "article_type_id":article_type_id,
                      "article_list":article_list,
                      "page_str":page_str,
                  }
                  )

def home(request,site):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    base_url = site+".html"
    tag_list = models.Tag.objects.filter(blog=blog)
    type_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    # article_list = models.Article.objects.filter(blog=blog).order_by("nid").all()
    data_count = models.Article.objects.filter(blog=blog).count()  # 需要展示的总个数
    page_obj = Pagination(request.GET.get('p'), data_count, per_page_count=4)  # 当前页码
    # 为了显示最新内容在最上面，需要加上order_by,参数加-就是倒序（desc），不加就是顺序（asc）
    article_list = models.Article.objects.filter(blog=blog).order_by('nid')[page_obj.start:page_obj.end]
    # page_str就是分页工具最后生成的那一排a标签，要传到前端去显示
    page_str = page_obj.page_str(base_url)
    return render(request,'home.html',{
        'blog':blog,
        "tag_list":tag_list,
        "type_list":type_list,
        "date_list":date_list,
        "article_list":article_list,
        "page_str":page_str,
    }
                  )


def filter(request,site,type,val):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    type_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    if type == "tag":
        article_list = models.Article.objects.filter(blog=blog,tag=val)
    elif type == "categroy":
        article_list = models.Article.objects.filter(blog=blog,categroy_id=val)

    elif type == "data":
        #mysql数据库用下面这个
        # article_list = models.Article.objects.filter(blog=blog).extra(
        # where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
        #sqlite用下面这个
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    return render(request,'home.html',{
        'blog':blog,
        "tag_list":tag_list,
        "type_list":type_list,
        "date_list":date_list,
        "article_list":article_list
    }
                  )

def detail(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    base_url = "/"+site+"/"+nid+".html"
    tag_list = models.Tag.objects.filter(blog_id=blog.bid)
    type_list = models.Category.objects.filter(blog_id=blog.bid)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    # article = models.Article.objects.filter(blog_id=blog.bid,nid=nid).first()
    article_detail = models.ArticleDetail.objects.filter(article_id=nid).first()
    # comment_list = models.Comment.objects.filter(article_id=nid).all()
    data_count = models.Comment.objects.filter(article_id=nid).count()
    page_obj = Pagination(request.GET.get('p'), data_count)
    comment_list = models.Comment.objects.filter(article_id=nid).order_by('-nid')[page_obj.start:page_obj.end]
    #page_str就是分页工具最后生成的那一排a标签，要传到前端去显示
    page_str = page_obj.page_str(base_url)

    return render(request,'home_detail.html',
                  {
                      "blog":blog,
                      "tag_list":tag_list,
                      "type_list":type_list,
                      "date_list":date_list,
                      "article":article_detail,
                      "comment_list":comment_list,
                      "page_str":page_str,
                  })