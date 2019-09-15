# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from io import BytesIO
from utils.check_code import create_validate_code
from web.forms.register import RegisterForm
from web.forms.login import LoginForm
from repository import models
import json

def register(request):
    if request.method == "GET":
        obj = RegisterForm(request)
        # print(666)
        return render(request,"register.html",{"obj":obj})
    elif request.method == "POST":
        obj = RegisterForm(request=request,data=request.POST)
        if obj.is_valid():
            values = obj.clean()
            print('vvvvvv', values)
            models.UserInfo.objects.create(
                username=values['username'],
                email=values['email'],
                password=values['password'],
            )
            return redirect('/login.html')

        else:
            error = obj.errors
            print(error)
            return render(request, "register.html", {"obj": obj})



def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    # print(code)
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        obj = LoginForm(request=request,data = request.POST)
        if obj.is_valid():
            username = request.POST.get('username')
            # print('username-------------',username)
            pwd = request.POST.get('password')
            # print('pwd---------------',pwd)
            userinfo = models.UserInfo.objects.filter(username=username,password=pwd).values(
                'nid','username','nickname','email','avatar','blog__bid','blog__site',
            ).first()
            # print('userinfo-------------------',userinfo)
            if not userinfo:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = userinfo
                if obj.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            print(obj.errors)
            if 'valid_code' in obj.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误------'
        return HttpResponse(json.dumps(result))

def logout(request):
    request.session['user_info'] = None
    return redirect('/')


