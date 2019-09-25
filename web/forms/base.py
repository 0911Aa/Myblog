# -*- coding: utf-8 -*-

class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        # 如果需要额外接收参数，要重写构造器函数
        # 这里额外接收一个参数，用于从request.sesssion中提取之前保存的验证码
        super(BaseForm, self).__init__(*args, **kwargs)
        self.request = request