# -*- coding: utf-8 -*-
# #注册
#
# import re
# from django.forms import Form
# from django.forms import widgets
# from django.forms import fields
# from django.core.exceptions import ValidationError
# #
# #
# def mobile_validate(value):
#     mobile_re = re.compile(r'^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$')
#     if not mobile_re.match(value):
#         raise ValidationError('密码格式错误')
#
# class RegisterForm(Form):
#     username = fields.CharField(required=True,
#         # widget=widgets.TextInput(attrs={"class": "form-control"}),
#         max_length=32,
#         min_length=2,
#         # error_messages={
#         #     "min_length":"用户名太短",
#         #     "max_length":"用户名过长",
#         #     "required":"用户名不能为空",
#         #
#         # }
#     )
#     password = fields.CharField(validators=[mobile_validate, ])
#     # password = fields.RegexField(
#     #     # widget=widgets.TextInput(attrs={"type": "password",
#     #     #                                 "class": "form-control"}),
#     #     regex='^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
#     #     # #需要特殊字符就用下面这个
#     #     # # regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
#     #     min_length=8,
#     #     max_length=32,
#     #     # error_messages={'required': '密码不能为空.',
#     #     #                 'invalid': '密码必须包含数字，字母',
#     #     #                 'min_length': "密码长度不能小于8个字符",
#     #     #                 'max_length': "密码长度不能大于32个字符"}
#     # )
#     confirmpwd = fields.RegexField(
#         # widget=widgets.TextInput(attrs={"type": "password",
#         #                                 "class": "form-control"}),
#         regex='^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
#         # #需要特殊字符就用下面这个
#         # # regex='^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
#         min_length=8,
#         max_length=32,
#         # error_messages={'required': '密码不能为空.',
#         #                 'invalid': '密码必须包含数字，字母',
#         #                 'min_length': "密码长度不能小于8个字符",
#         #                 'max_length': "密码长度不能大于32个字符"},
#     )
#     email = fields.EmailField(required=True,
#         # widget=widgets.TextInput(attrs={"type": "email",
#         #                                 "class": "form-control",
#         #                                 "id": "exampleInputEmail1",}),
#         # error_messages={
#         #     "required":"邮箱不能为空",
#         #     'invalid': u'邮箱格式错误',
#         # }
#
#     )
#     verification_code = fields.CharField(
#         # widget=widgets.TextInput(attrs={"class": "form-control"})
#     )
#
#     #钩子函数，上面所有匹配完成后执行
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         pwd1 = cleaned_data["password"]
#         pwd2 = cleaned_data["confirmpwd"]
#         if pwd1 == pwd2:
#             pass
#         else:
#             #否则报错，用专属报错
#             from django.core.exceptions import ValidationError
#             raise ValidationError('密码不一致')
#
#
#
# def register(request):
#     if request.method == "GET":
#         obj = RegisterForm()
#         return render(request,"register.html",{"obj":obj})
#     elif request.method == "POST":
#         obj = RegisterForm(request.POST)
#         if obj.is_valid():
#             values = obj.clean()
#             print(values)
#             return redirect('/')
#         else:
#             error = obj.errors
#             print(error)
#         return render(request, "register.html", {"obj": obj})


from django import forms  # 导入表单模块
from django.core.exceptions import ValidationError
from web.forms.base import BaseForm
from repository import models


class RegisterForm(BaseForm,forms.Form):  # 自定义表单类，并继承forms.Form
    email = forms.EmailField(
        error_messages={
            "required": "邮箱不能为空",
            'invalid': u'邮箱格式错误',
        },
        widget=forms.EmailInput(attrs={"class": "form-control"}))

    username = forms.CharField(
        min_length=2,
        max_length=12,
        error_messages={
            "min_length":"用户名长度不能小于2",
            "max_length":"用户名长度不能大于12",
            "required": "用户名不能为空",
            'invalid': u'用户名格式错误',
        },

        widget=forms.TextInput(attrs={"class": "form-control"}))

    password = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={"class": "form-control"}))

    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={"class": "form-control"}))

    valid_code = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))


    # 自定义方法（局部钩子），密码必须包含字母和数字
    def clean_password(self):
        if self.cleaned_data.get('password').isdigit() or self.cleaned_data.get('password').isalpha():
            raise ValidationError('密码必须包含数字和字母')
        else:
            return self.cleaned_data['password']

    def clean_valid_code(self):  # 检验验证码正确；之前生成的验证码保存在了了session中
        # print(self.cleaned_data.get('valid_code').upper())
        # print(self.request.session.get('CheckCode').upper())
        if self.cleaned_data.get('valid_code').upper() == self.request.session.get('CheckCode').upper():
            return self.cleaned_data['valid_code']
        else:
            raise ValidationError('验证码不正确')

    def clean_username(self):
        user_info = models.UserInfo.objects.filter(username=self.cleaned_data.get('username')).first()
        if user_info:
            raise ValidationError('用户名重复')
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        user_info = models.UserInfo.objects.filter(email=self.cleaned_data.get('email')).first()
        if user_info:
            raise ValidationError('此邮箱已经注册过')
        else:
            return self.cleaned_data['email']

    # 自定义方法（全局钩子, 检验两个字段），检验两次密码一致;
    def clean(self):
        print(self.cleaned_data)
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('密码不一致')
        else:
            # pass
            return self.cleaned_data

    # 注意，上面的字典取值用get, 因为假如在clean_password中判断失败，那么没有返回值，最下面的clean方法直接取值就会失败s　