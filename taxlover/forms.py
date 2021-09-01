from importlib._common import _

from django import forms
from django.forms import TextInput

from .models import TaxPayer, Document, Salary


class TaxPayerForm(forms.ModelForm):

    class Meta:
        model = TaxPayer
        fields = ['name', 'e_tin']


class UploadSalaryStatementForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['basic', 'house_rent', 'medical', 'conveyance', 'lfa']
        widgets = {
            'basic': TextInput(attrs={'class': 'form-control', 'onblur': 'inputBlur(this)'}),
            'house_rent': TextInput(attrs={'class': 'form-control', 'onblur': 'inputBlur(this)'}),
            'medical': TextInput(attrs={'class': 'form-control', 'onblur': 'inputBlur(this)'}),
        }
