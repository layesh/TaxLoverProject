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
        fields = ['basic', 'house_rent', 'medical', 'conveyance', 'lfa', 'total_bonus', 'employers_contribution_to_pf']
        widgets = {
            'basic': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'house_rent': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'medical': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'conveyance': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'lfa': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'total_bonus': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'employers_contribution_to_pf': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
        }
