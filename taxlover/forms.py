from django import forms
from django.forms import TextInput

from .models import TaxPayer, Document, Salary, OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, \
    ADVANCE_TAX_PAID_TYPE, TaxRefund, AgriculturalProperty, Investment, MotorVehicle


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
                  'interest_income_from_wedb', 'us_dollar_premium_investment_bond',
                  'pound_sterling_premium_investment_bond', 'euro_premium_investment_bond',
                  'sanchaypatra_income', 'others']
        widgets = {
            'interest_from_mutual_fund_unit_fund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'cash_dividend_from_company_listed_in_stock_exchange': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'interest_income_from_wedb': TextInput(
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


class TaxRebateForm(forms.ModelForm):
    class Meta:
        model = TaxRebate
        fields = ['life_insurance_premium', 'life_insurance_premium_policy_value', 'contribution_to_pf_as_per_act_1925',
                  'self_and_employers_contribution_to_pf', 'contribution_to_super_annuation_fund',
                  'investment_in_approved_debenture_or_stock_or_shares', 'contribution_to_dps',
                  'contribution_to_benevolent_fund_and_group_insurance_premium', 'contribution_to_zakat_fund',
                  'investment_in_savings_certificates_sanchaypatra', 'investment_in_bangladesh_govt_treasury_bond',
                  'donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation',
                  'donation_to_a_charitable_hospital_recognized_by_nbr',
                  'donation_to_organizations_set_up_for_the_welfare_of_retarded_people',
                  'contribution_to_national_level_institution_set_up_in_memory_of_liberation_war',
                  'contribution_to_liberation_war_museum', 'contribution_to_aga_khan_development_network',
                  'contribution_to_asiatic_society_bangladesh', 'donation_to_icddrb', 'donation_to_crp',
                  'donation_to_educational_institution_recognized_by_government',
                  'contribution_to_ahsania_mission_cancer_hospital', 'mutual_fund']
        widgets = {
            'life_insurance_premium': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'life_insurance_premium_policy_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_pf_as_per_act_1925': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'self_and_employers_contribution_to_pf': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_super_annuation_fund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'investment_in_approved_debenture_or_stock_or_shares': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_dps': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_benevolent_fund_and_group_insurance_premium': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_zakat_fund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'investment_in_savings_certificates_sanchaypatra': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'investment_in_bangladesh_govt_treasury_bond': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_a_charitable_hospital_recognized_by_nbr': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_organizations_set_up_for_the_welfare_of_retarded_people': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_national_level_institution_set_up_in_memory_of_liberation_war': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_liberation_war_museum': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_aga_khan_development_network': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_asiatic_society_bangladesh': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_icddrb': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_crp': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_to_educational_institution_recognized_by_government': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'contribution_to_ahsania_mission_cancer_hospital': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'mutual_fund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),

        }


class DeductionAtSourceForm(forms.ModelForm):
    class Meta:
        model = DeductionAtSource
        fields = ['id', 'description', 'tax_deducted_at_source']
        widgets = {
            'id': forms.HiddenInput(),
            'description': TextInput(
                attrs={'class': 'form-control'}),
            'tax_deducted_at_source': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class AdvanceTaxPaidForm(forms.ModelForm):
    class Meta:
        model = AdvanceTax
        fields = ['id', 'type', 'description', 'advance_paid_tax']
        widgets = {
            'id': forms.HiddenInput(),
            'type': forms.Select(
                attrs={'class': 'form-select dropdown-width-165'}),
            'description': TextInput(
                attrs={'class': 'form-control', 'id': 'id_apt_description'}),
            'advance_paid_tax': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class TaxRefundForm(forms.ModelForm):
    class Meta:
        model = TaxRefund
        fields = ['refund']
        widgets = {
            'refund': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class AgriculturalPropertyForm(forms.ModelForm):
    class Meta:
        model = AgriculturalProperty
        fields = ['id', 'description', 'value']
        widgets = {
            'id': forms.HiddenInput(),
            'description': TextInput(
                attrs={'class': 'form-control', 'id': 'id_ap_description'}),
            'value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['type', 'description', 'value']
        widgets = {
            'type': forms.Select(
                attrs={'class': 'form-select'}),
            'description': TextInput(
                attrs={'class': 'form-control'}),
            'value': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'})
        }


class MotorVehicleForm(forms.ModelForm):
    class Meta:
        model = MotorVehicle
        fields = ['brand_or_type', 'reg_no', 'engine_capacity', 'value']
        widgets = {
            'brand_or_type': TextInput(
                attrs={'class': 'form-control'}),
            'reg_no': TextInput(
                attrs={'class': 'form-control'}),
            'engine_capacity': TextInput(
                attrs={'class': 'form-control'}),
            'value': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'})
        }
