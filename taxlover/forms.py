from django import forms
from django.forms import TextInput

from .models import TaxPayer, Document, Salary, OtherIncome


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
            'basic': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'house_rent': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'medical': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'conveyance': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'lfa': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'total_bonus': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'employers_contribution_to_pf': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
        }


class OtherIncomeForm(forms.ModelForm):
    class Meta:
        model = OtherIncome
        fields = ['interest_from_mutual_fund_unit_fund', 'cash_dividend_from_company_listed_in_stock_exchange',
                  'interest_income_from_wedb', 'conveyance', 'us_dollar_premium_investment_bond',
                  'pound_sterling_premium_investment_bond', 'euro_premium_investment_bond',
                  'sanchaypatra_income', 'others']
        widgets = {
            'interest_from_mutual_fund_unit_fund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'cash_dividend_from_company_listed_in_stock_exchange': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'interest_income_from_wedb': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'conveyance': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'us_dollar_premium_investment_bond': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'pound_sterling_premium_investment_bond': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'euro_premium_investment_bond': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'sanchaypatra_income': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'others': TextInput(attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }
