from decimal import Decimal

from taxlover.constants import INTEREST_FROM_MUTUAL_FUND_YEARLY_EXEMPTED_RATE, CASH_DIVIDEND_YEARLY_EXEMPTED_RATE, \
    DPS_MAX_ALLOWED_RATE
from taxlover.models import OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, TaxRefund, AgriculturalProperty
from taxlover.services.salary_service import get_current_financial_year_salary_by_payer
from taxlover.utils import get_income_years


def save_assets(latest_assets, source, answer, request):
    show_success_message = False

    if source == 'business_capital':
        show_success_message = True
        if answer == 'yes':
            latest_assets.business_capital = True
        elif answer == 'no':
            latest_assets.business_capital = False
    elif source == 'directors_shareholding_assets':
        show_success_message = True
        if answer == 'yes':
            latest_assets.directors_shareholding_assets = True
        elif answer == 'no':
            latest_assets.directors_shareholding_assets = False
    elif source == 'non_agricultural_property':
        show_success_message = True
        if answer == 'yes':
            latest_assets.non_agricultural_property = True
        elif answer == 'no':
            latest_assets.non_agricultural_property = False
    elif source == 'agricultural_property':
        show_success_message = True
        if answer == 'yes':
            latest_assets.agricultural_property = True
        elif answer == 'no':
            latest_assets.agricultural_property = False
    # elif source == 'business':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.business = True
    #     elif answer == 'no':
    #         latest_assets.business = False
    # elif source == 'share_of_profit_in_firm':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.share_of_profit_in_firm = True
    #     elif answer == 'no':
    #         latest_assets.share_of_profit_in_firm = False
    # elif source == 'spouse_or_child':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.spouse_or_child = True
    #     elif answer == 'no':
    #         latest_assets.spouse_or_child = False
    # elif source == 'capital_gains':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.capital_gains = True
    #     elif answer == 'no':
    #         latest_assets.capital_gains = False
    # elif source == 'other_sources':
    #     if answer == 'yes':
    #         latest_assets.other_sources = True
    #     elif answer == 'no':
    #         show_success_message = True
    #         latest_assets.other_sources = False
    #         other_income = get_current_financial_year_other_income_by_payer(request.user.id)
    #         if other_income:
    #             other_income.delete()
    # elif source == 'foreign_income':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.foreign_income = True
    #     elif answer == 'no':
    #         latest_assets.foreign_income = False
    # elif source == 'tax_rebate':
    #     if answer == 'yes':
    #         latest_assets.tax_rebate = True
    #     elif answer == 'no':
    #         show_success_message = True
    #         latest_assets.tax_rebate = False
    #         tax_rebate = get_current_financial_year_tax_rebate_by_payer(request.user.id)
    #         if tax_rebate:
    #             tax_rebate.delete()
    # elif source == 'tax_deducted_at_source':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.tax_deducted_at_source = True
    #     elif answer == 'no':
    #         latest_assets.tax_deducted_at_source = False
    #         deductions = get_current_financial_year_deduction_at_source_by_payer(request.user.id)
    #         if deductions:
    #             deductions.delete()
    # elif source == 'advance_paid_tax':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.advance_paid_tax = True
    #     elif answer == 'no':
    #         latest_assets.advance_paid_tax = False
    #         advances = get_current_financial_year_advance_tax_paid_by_payer(request.user.id)
    #         if advances:
    #             advances.delete()
    # elif source == 'adjustment_of_tax_refund':
    #     show_success_message = True
    #     if answer == 'yes':
    #         latest_assets.adjustment_of_tax_refund = True
    #     elif answer == 'no':
    #         latest_assets.adjustment_of_tax_refund = False
    #         refunds = get_current_financial_year_tax_refund_by_payer(request.user.id)
    #         if refunds:
    #             refunds.delete()

    latest_assets.save()

    return show_success_message


def get_current_financial_year_agricultural_property_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return AgriculturalProperty.objects.filter(tax_payer_id=payer_id,
                                               financial_year_beg=financial_year_beg,
                                               financial_year_end=financial_year_end)
