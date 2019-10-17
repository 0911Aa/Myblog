# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
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
    elif request.method == "POST":
        form = ArticleForm(request,data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            tags = form.cleaned_data.pop('tags')     #取出数据中的tags
            content = form.cleaned_data.pop('content') #取出数据中的content

            form.cleaned_data['blog_id'] = request.session['user_info']['blog__bid']
            obj = models.Article.objects.create(**form.cleaned_data)
            models.ArticleDetail.objects.create(content=content,article=obj)
            tag_list = []
            for tag_id in tags:
                tag_id = int(tag_id)
                tag_list.append(models.Tag2Article(article_id=obj.nid, tag_id=tag_id))
            models.Tag2Article.objects.bulk_create(tag_list)  #批量导入数据
            return redirect('/backend/article-0-0.html')
        else:
            return render(request,"backend_add_article.html",{"form":form})
    else:
        return redirect("/")

@check_login
def edit_article(request,nid):
    blog_id = request.session["user_info"]["blog__bid"]
    if request.method == "GET":

        obj = models.Article.objects.filter(nid=nid,blog_id=blog_id).first()
        content = models.ArticleDetail.objects.filter(article=obj).values('content').first().get("content")

        # print(content)
        if not obj:
            # pass
            return render(request, 'backend_no_article.html')
        tags = obj.tag.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'nid': obj.nid,
            'title': obj.title,
            'summary': obj.summary,
            'category_id': obj.category_id,
            'article_type_id': obj.article_type_id,
            'content': content,
            'tags': tags}
        form = ArticleForm(request,data=init_dict)
        return render(request,"backend_edit_article.html",{"form":form,'nid': nid})
    elif request.method == "POST":
        form = ArticleForm(request,data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
            if not obj:
                # pass
                return render(request, 'backend_no_article.html')
            # print(form.cleaned_data)
            tags = form.cleaned_data.pop('tags')     #取出数据中的tags
            content = form.cleaned_data.pop('content') #取出数据中的content
            models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
            models.ArticleDetail.objects.filter(article=obj).update(content=content)
            models.Tag2Article.objects.filter(article=obj).delete()
            tag_list = []
            for tag_id in tags:
                tag_id = int(tag_id)
                tag_list.append(models.Tag2Article(article_id=obj.nid, tag_id=tag_id))
            models.Tag2Article.objects.bulk_create(tag_list)  #批量导入数据
            return redirect('/backend/article-0-0.html')
        else:
            return render(request,"backend_edit_article.html",{"form":form,'nid': nid})

@check_login
def delete_article(request,nid):
    if request.method == "GET":
        models.Article.objects.filter(nid=nid).delete()
        return redirect('/backend/article-0-0.html')
    else:
        return HttpResponse("删除文章出错")