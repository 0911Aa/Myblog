# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from backend.auth.auth import check_login
from backend.forms.troubles import TroubleForm
import datetime,uuid
from repository import models

@check_login
def trouble(request):
    current_user_id = request.session['user_info']["nid"]
    trouble_list = models.IssueInfo.objects.filter(user_id=current_user_id).order_by("-status")
    data_count = models.IssueInfo.objects.filter(user_id=current_user_id).count()
    return render(request,'backend_trouble.html',{"trouble_list":trouble_list,"data_count":data_count})

@check_login
def trouble_create(request):
    if request.method == "GET":
        form = TroubleForm()
        return render(request,'backend_trouble_create.html',{"form":form})
    elif request.method == "POST":
        form = TroubleForm(request.POST)
        if form.is_valid():
            dic = {}
            dic["uuid"] = uuid.uuid4()
            dic['create_time'] = datetime.datetime.now()
            dic["user_id"] = request.session['user_info']["nid"]
            dic["status"] = 1
            dic.update(form.cleaned_data)
            models.IssueInfo.objects.create(**dic)
            return redirect("/backend/trouble.html")
        else:
            return render(request, 'backend_trouble_create.html', {"form": form})

@check_login
def trouble_edit(request,nid):
    if request.method == "GET":
        obj = models.IssueInfo.objects.filter(id=nid,status=1).only("id","title","detail").first()
        if not obj:
            ## initial 仅初始化,不会验证数据
            return HttpResponse("已处理中的保单章无法修改..")
        form = TroubleForm(initial={"title":obj.title,"detail":obj.detail})
        return render(request,"backend_trouble_edit.html",{"form":form,"nid":nid})
    elif request.method == "POST":
        form = TroubleForm(data=request.POST)
        if form.is_valid():
            v = models.IssueInfo.objects.filter(id=nid,status=1).update(**form.cleaned_data)
            if not v:
                return HttpResponse("故障正在处理中...")
            return redirect("/backend/trouble.html")
        else:
            return render(request,'backend_trouble_edit.html',{"form":form,"nid":nid})
    else:
        return redirect("/backend/trouble.html")

@check_login
def trouble_delete(request,nid):
    v = models.IssueInfo.objects.filter(id=nid,status=1).delete()
    if v:
        return redirect("/backend/trouble.html")
    else:
        return HttpResponse("开始处理的故障无法删除")

