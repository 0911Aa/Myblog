# -*- coding: utf-8 -*-
from django import forms  # 导入表单模块
from django.core.exceptions import ValidationError
from web.forms.base import BaseForm


class LoginForm(BaseForm,forms.Form):  # 自定义表单类，并继承forms.Form

    username = forms.CharField(
        error_messages={
            "required": "用户名不能为空",
            'invalid': u'用户名格式错误',
        },

        widget=forms.TextInput(attrs={"class": "form-control"}))

    password = forms.CharField(min_length=6, widget=forms.PasswordInput(
        attrs={"class": "form-control"}),
       error_messages={
           "required": "密码不能为空",
       },
        )


    valid_code = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}),
        error_messages={
            "required": "验证码不能为空",}
    )

    # 自定义方法（局部钩子）
    def clean_valid_code(self):  # 检验验证码正确；之前生成的验证码保存在了了session中
        print(self.cleaned_data)
        # print(self.request.session.get('CheckCode').upper())
        if self.cleaned_data.get('valid_code').upper() == self.request.session.get('CheckCode').upper():
            return self.cleaned_data['valid_code']
        else:
            raise ValidationError('验证码不正确')