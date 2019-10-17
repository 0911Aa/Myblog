# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets
from repository import models

class TroubleForm(django_forms.Form):

    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )

    detail = django_fields.CharField(
        # required=False,
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'})
    )
