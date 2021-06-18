from django import forms
from .models import TaxPayer


class TaxPayerForm(forms.ModelForm):

    class Meta:
        model = TaxPayer
        fields = ['name', 'e_tin']
