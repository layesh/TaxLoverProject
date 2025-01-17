from decimal import Decimal

from django.db.models import Sum

from taxlover.constants import INTEREST_FROM_MUTUAL_FUND_YEARLY_EXEMPTED_RATE, CASH_DIVIDEND_YEARLY_EXEMPTED_RATE, \
    DPS_MAX_ALLOWED_RATE
from taxlover.models import OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, TaxRefund, InterestOnSecurities
from taxlover.services.salary_service import get_current_financial_year_salary_by_payer
from taxlover.utils import get_income_years


def save_income(latest_income, source, answer, request):
    show_success_message = False

    if source == 'salary':
        if answer == 'yes':
            latest_income.salary = True
        elif answer == 'no':
            show_success_message = True
            latest_income.salary = False
            salary = get_current_financial_year_salary_by_payer(request.user.id)
            if salary:
                salary.delete()
    elif source == 'interest_on_security':
        show_success_message = True
        if answer == 'yes':
            latest_income.interest_on_security = True
        elif answer == 'no':
            latest_income.interest_on_security = False
    elif source == 'rental_property':
        show_success_message = True
        if answer == 'yes':
            latest_income.rental_property = True
        elif answer == 'no':
            latest_income.rental_property = False
    elif source == 'agriculture':
        show_success_message = True
        if answer == 'yes':
            latest_income.agriculture = True
        elif answer == 'no':
            latest_income.agriculture = False
    elif source == 'business':
        show_success_message = True
        if answer == 'yes':
            latest_income.business = True
        elif answer == 'no':
            latest_income.business = False
    elif source == 'share_of_profit_in_firm':
        show_success_message = True
        if answer == 'yes':
            latest_income.share_of_profit_in_firm = True
        elif answer == 'no':
            latest_income.share_of_profit_in_firm = False
    elif source == 'spouse_or_child':
        show_success_message = True
        if answer == 'yes':
            latest_income.spouse_or_child = True
        elif answer == 'no':
            latest_income.spouse_or_child = False
    elif source == 'capital_gains':
        show_success_message = True
        if answer == 'yes':
            latest_income.capital_gains = True
        elif answer == 'no':
            latest_income.capital_gains = False
    elif source == 'other_sources':
        if answer == 'yes':
            latest_income.other_sources = True
        elif answer == 'no':
            show_success_message = True
            latest_income.other_sources = False
            other_income = get_current_financial_year_other_income_by_payer(request.user.id)
            if other_income:
                other_income.delete()
    elif source == 'foreign_income':
        show_success_message = True
        if answer == 'yes':
            latest_income.foreign_income = True
        elif answer == 'no':
            latest_income.foreign_income = False
    elif source == 'tax_rebate':
        if answer == 'yes':
            latest_income.tax_rebate = True
        elif answer == 'no':
            show_success_message = True
            latest_income.tax_rebate = False
            tax_rebate = get_current_financial_year_tax_rebate_by_payer(request.user.id)
            if tax_rebate:
                tax_rebate.delete()
    elif source == 'tax_deducted_at_source':
        show_success_message = True
        if answer == 'yes':
            latest_income.tax_deducted_at_source = True
        elif answer == 'no':
            latest_income.tax_deducted_at_source = False
            deductions = get_current_financial_year_deduction_at_source_by_payer(request.user.id)
            if deductions:
                deductions.delete()
    elif source == 'advance_paid_tax':
        show_success_message = True
        if answer == 'yes':
            latest_income.advance_paid_tax = True
        elif answer == 'no':
            latest_income.advance_paid_tax = False
            advances = get_current_financial_year_advance_tax_paid_by_payer(request.user.id)
            if advances:
                advances.delete()
    elif source == 'adjustment_of_tax_refund':
        show_success_message = True
        if answer == 'yes':
            latest_income.adjustment_of_tax_refund = True
        elif answer == 'no':
            latest_income.adjustment_of_tax_refund = False
            refunds = get_current_financial_year_tax_refund_by_payer(request.user.id)
            if refunds:
                refunds.delete()

    latest_income.save()

    return show_success_message


def get_current_financial_year_other_income_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return OtherIncome.objects.filter(tax_payer_id=payer_id,
                                      financial_year_beg=financial_year_beg,
                                      financial_year_end=financial_year_end).first()


def get_interest_from_mutual_fund_exempted(interest_from_mutual_fund):
    return Decimal(min(INTEREST_FROM_MUTUAL_FUND_YEARLY_EXEMPTED_RATE, Decimal(interest_from_mutual_fund)))


def get_cash_dividend_exempted(cash_dividend):
    return Decimal(min(CASH_DIVIDEND_YEARLY_EXEMPTED_RATE, Decimal(cash_dividend)))


def get_total_other_income_taxable(other_income):
    return other_income.get_interest_from_mutual_fund_unit_fund - \
           get_interest_from_mutual_fund_exempted(other_income.get_interest_from_mutual_fund_unit_fund) + \
           other_income.get_cash_dividend_from_company_listed_in_stock_exchange - \
           get_cash_dividend_exempted(other_income.get_cash_dividend_from_company_listed_in_stock_exchange) + \
           other_income.get_sanchaypatra_income + other_income.get_others


def get_current_financial_year_tax_rebate_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return TaxRebate.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end).first()


def get_life_insurance_premium_allowed(life_insurance_premium, life_insurance_premium_policy_value):
    return Decimal(min(float(life_insurance_premium_policy_value) * 0.1, float(life_insurance_premium)))


def get_contribution_to_dps_allowed(contribution_to_dps):
    return Decimal(min(DPS_MAX_ALLOWED_RATE, Decimal(contribution_to_dps)))


def get_total_allowed_amount(tax_rebate):
    return get_life_insurance_premium_allowed(tax_rebate.get_life_insurance_premium,
                                              tax_rebate.get_life_insurance_premium_policy_value) + \
           tax_rebate.get_contribution_to_pf_as_per_act_1925 + \
           tax_rebate.get_self_and_employers_contribution_to_pf + \
           tax_rebate.get_contribution_to_super_annuation_fund + \
           tax_rebate.get_investment_in_approved_debenture_or_stock_or_shares + \
           get_contribution_to_dps_allowed(tax_rebate.get_contribution_to_dps) + \
           tax_rebate.get_contribution_to_benevolent_fund_and_group_insurance_premium + \
           tax_rebate.get_contribution_to_zakat_fund + \
           tax_rebate.get_investment_in_savings_certificates_sanchaypatra + \
           tax_rebate.get_investment_in_bangladesh_govt_treasury_bond + \
           tax_rebate.get_donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation + \
           tax_rebate.get_donation_to_a_charitable_hospital_recognized_by_nbr + \
           tax_rebate.get_donation_to_organizations_set_up_for_the_welfare_of_retarded_people + \
           tax_rebate.get_contribution_to_national_level_institution_set_up_in_memory_of_liberation_war + \
           tax_rebate.get_contribution_to_liberation_war_museum + \
           tax_rebate.get_contribution_to_aga_khan_development_network + \
           tax_rebate.get_contribution_to_asiatic_society_bangladesh + tax_rebate.get_donation_to_icddrb + \
           tax_rebate.get_donation_to_crp + \
           tax_rebate.get_donation_to_educational_institution_recognized_by_government + \
           tax_rebate.get_contribution_to_ahsania_mission_cancer_hospital + tax_rebate.get_mutual_fund


def get_current_financial_year_deduction_at_source_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return DeductionAtSource.objects.filter(tax_payer_id=payer_id,
                                            financial_year_beg=financial_year_beg,
                                            financial_year_end=financial_year_end)


def get_current_financial_year_advance_tax_paid_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return AdvanceTax.objects.filter(tax_payer_id=payer_id,
                                     financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end)


def get_current_financial_year_tax_refund_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return TaxRefund.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end).first()


def get_interest_on_securities_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return InterestOnSecurities.objects.filter(tax_payer_id=payer_id,
                                               financial_year_beg=financial_year_beg,
                                               financial_year_end=financial_year_end)


def get_total_interest_on_securities_value(interest_on_securities):
    total = interest_on_securities.aggregate(Sum('amount'))

    return total['amount__sum'] if total['amount__sum'] is not None else 0
