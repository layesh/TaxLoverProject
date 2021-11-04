from django import forms
from django.forms import TextInput

from .models import TaxPayer, Document, Salary, OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, \
    ADVANCE_TAX_PAID_TYPE, TaxRefund, AgriculturalProperty, Investment, MotorVehicle, Furniture, Jewellery, \
    ElectronicEquipment, CashAssets, OtherAssets, OtherAssetsReceipt, PreviousYearNetWealth, Mortgage, UnsecuredLoan, \
    BankLoan, OtherLiability, Expense


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
        fields = ['deduction_description', 'tax_deducted_at_source']
        widgets = {
            'deduction_description': TextInput(
                attrs={'class': 'form-control'}),
            'tax_deducted_at_source': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class AdvanceTaxPaidForm(forms.ModelForm):
    class Meta:
        model = AdvanceTax
        fields = ['type', 'advance_description', 'advance_paid_tax']
        widgets = {
            'type': forms.Select(
                attrs={'class': 'form-select dropdown-width-165'}),
            'advance_description': TextInput(
                attrs={'class': 'form-control'}),
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
        fields = ['property_description', 'property_value']
        widgets = {
            'property_description': TextInput(
                attrs={'class': 'form-control'}),
            'property_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['type', 'description', 'value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'value': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'})
        }


class MotorVehicleForm(forms.ModelForm):
    class Meta:
        model = MotorVehicle
        fields = ['brand_or_type', 'reg_no', 'engine_capacity', 'value']
        widgets = {
            'brand_or_type': TextInput(attrs={'class': 'form-control'}),
            'reg_no': TextInput(attrs={'class': 'form-control'}),
            'engine_capacity': TextInput(attrs={'class': 'form-control'}),
            'value': TextInput(attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'})
        }


class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = ['furniture_description', 'furniture_value']
        widgets = {
            'furniture_description': TextInput(attrs={'class': 'form-control'}),
            'furniture_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class JewelleryForm(forms.ModelForm):
    class Meta:
        model = Jewellery
        fields = ['jewellery_description', 'jewellery_value']
        widgets = {
            'jewellery_description': TextInput(attrs={'class': 'form-control'}),
            'jewellery_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class ElectronicEquipmentForm(forms.ModelForm):
    class Meta:
        model = ElectronicEquipment
        fields = ['equipment_description', 'equipment_value']
        widgets = {
            'equipment_description': TextInput(attrs={'class': 'form-control'}),
            'equipment_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class CashAssetsForm(forms.ModelForm):
    class Meta:
        model = CashAssets
        fields = ['cash_in_hand', 'cash_at_bank', 'other_fund', 'other_deposits']
        widgets = {
            'cash_in_hand': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'cash_at_bank': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'other_fund': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'}),
            'other_deposits': TextInput(
                attrs={'class': 'form-control', 'onblur': 'onInputBlurred(this)'})
        }


class OtherAssetsForm(forms.ModelForm):
    class Meta:
        model = OtherAssets
        fields = ['asset_description', 'asset_value']
        widgets = {
            'asset_description': TextInput(attrs={'class': 'form-control'}),
            'asset_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class OtherAssetsReceiptForm(forms.ModelForm):
    class Meta:
        model = OtherAssetsReceipt
        fields = ['other_asset_description', 'other_asset_value']
        widgets = {
            'other_asset_description': TextInput(attrs={'class': 'form-control'}),
            'other_asset_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class PreviousYearNetWealthForm(forms.ModelForm):
    class Meta:
        model = PreviousYearNetWealth
        fields = ['wealth_value']
        widgets = {
            'wealth_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class MortgageForm(forms.ModelForm):
    class Meta:
        model = Mortgage
        fields = ['mortgage_description', 'mortgage_value']
        widgets = {
            'mortgage_description': TextInput(
                attrs={'class': 'form-control'}),
            'mortgage_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class UnsecuredLoanForm(forms.ModelForm):
    class Meta:
        model = UnsecuredLoan
        fields = ['unsecured_loan_description', 'unsecured_loan_value']
        widgets = {
            'unsecured_loan_description': TextInput(
                attrs={'class': 'form-control'}),
            'unsecured_loan_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class BankLoanForm(forms.ModelForm):
    class Meta:
        model = BankLoan
        fields = ['bank_loan_description', 'bank_loan_value']
        widgets = {
            'bank_loan_description': TextInput(
                attrs={'class': 'form-control'}),
            'bank_loan_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class OtherLiabilityForm(forms.ModelForm):
    class Meta:
        model = OtherLiability
        fields = ['other_liability_description', 'other_liability_value']
        widgets = {
            'other_liability_description': TextInput(
                attrs={'class': 'form-control'}),
            'other_liability_value': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'})
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['food_expense', 'food_expense_comment',
                  'accommodation_expense', 'accommodation_expense_comment',
                  'transportation_expense', 'transportation_expense_comment',
                  'other_transportation_expense', 'other_transportation_expense_comment',
                  'electricity_expense', 'electricity_expense_comment',
                  'gas_expense', 'gas_expense_comment',
                  'water_expense', 'water_expense_comment',
                  'telephone_expense', 'telephone_expense_comment',
                  'other_household_expense', 'other_household_expense_comment',
                  'children_education_expense', 'children_education_expense_comment',
                  'travel_expense', 'travel_expense_comment',
                  'festival_expense', 'festival_expense_comment',
                  'donation_expense', 'donation_expense_comment',
                  'other_special_expense', 'other_special_expense_comment',
                  'other_expense', 'other_expense_comment',
                  'tax_at_source_expense', 'tax_at_source_expense_comment',
                  'last_year_paid_tax_expense', 'last_year_paid_tax_expense_comment',
                  'loss_expense', 'loss_expense_comment',
                  'gift_expense', 'gift_expense_comment']
        widgets = {
            'food_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'food_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'accommodation_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'accommodation_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'transportation_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'transportation_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'other_transportation_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'other_transportation_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'electricity_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'electricity_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'gas_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'gas_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'water_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'water_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'telephone_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'telephone_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'other_household_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'other_household_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'children_education_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'children_education_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'travel_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'travel_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'festival_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'festival_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'donation_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'donation_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'other_special_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'other_special_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'other_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'other_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'tax_at_source_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'tax_at_source_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'last_year_paid_tax_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'last_year_paid_tax_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'loss_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'loss_expense_comment': TextInput(attrs={'class': 'form-control'}),
            'gift_expense': TextInput(
                attrs={'class': 'form-control text-align-right', 'onblur': 'onInputBlurred(this)'}),
            'gift_expense_comment': TextInput(attrs={'class': 'form-control'})
        }
