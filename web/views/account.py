# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from io import BytesIO
from utils.check_code import create_validate_code
from web.forms.register import RegisterForm
from web.forms.login import LoginForm

def register(request):
    if request.method == "GET":
        obj = RegisterForm(request)
        # print(666)
        return render(request,"register.html",{"obj":obj})
    elif request.method == "POST":
        obj = RegisterForm(request.POST)
        if obj.is_valid():
            values = obj.clean()
            print('vvvvvv',values)
            return redirect('/')
        else:
            error = obj.errors
            print(error)
        return redirect('/')
        # return render(request, "index.html", {"obj": obj})


def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    print(code)
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        obj = LoginForm(request=request,)

