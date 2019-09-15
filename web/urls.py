# -*- coding: utf-8 -*-
from django.conf.urls import url
from web.views import home,account
from django.urls import re_path,path

urlpatterns = [
    # url(r'^', home.index),
    path('',home.index),
    url(r'^all/(?P<article_type_id>\d+).html$', home.index, name='index'),
    path('register.html',account.register),
    path('create_check_code',account.check_code),
    path('login.html',account.login),
    path('logout.html',account.logout),
    re_path(r'^(?P<site>\w+).html$', home.home),
    re_path(r'^(?P<site>\w+)/(?P<type>((tag)|(categroy)|(data)))/(?P<val>\w+-*\w*).html$',
            home.filter),
    re_path(r'^(?P<site>\w+)/(?P<nid>\d+).html',home.detail),
]
