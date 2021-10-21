from decimal import Decimal

from taxlover.constants import INTEREST_FROM_MUTUAL_FUND_YEARLY_EXEMPTED_RATE, CASH_DIVIDEND_YEARLY_EXEMPTED_RATE, \
    DPS_MAX_ALLOWED_RATE
from taxlover.models import OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, TaxRefund, AgriculturalProperty, \
    Investment, MotorVehicle
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
    elif source == 'investments':
        if answer == 'yes':
            latest_assets.investments = True
        elif answer == 'no':
            show_success_message = True
            latest_assets.investments = False
            investments = get_current_financial_year_investments_by_payer(request.user.id)
            if investments:
                investments.delete()
    elif source == 'motor_vehicle':
        if answer == 'yes':
            latest_assets.motor_vehicle = True
        elif answer == 'no':
            show_success_message = True
            latest_assets.motor_vehicle = False
            investments = get_current_financial_year_motor_vehicle_by_payer(request.user.id)
            if investments:
                investments.delete()
    elif source == 'furniture':
        show_success_message = True
        if answer == 'yes':
            latest_assets.furniture = True
        elif answer == 'no':
            latest_assets.furniture = False
    elif source == 'jewellery':
        show_success_message = True
        if answer == 'yes':
            latest_assets.jewellery = True
        elif answer == 'no':
            latest_assets.jewellery = False
    elif source == 'electronic_equipment':
        show_success_message = True
        if answer == 'yes':
            latest_assets.electronic_equipment = True
        elif answer == 'no':
            latest_assets.electronic_equipment = False
    elif source == 'cash_assets':
        show_success_message = True
        if answer == 'yes':
            latest_assets.cash_assets = True
        elif answer == 'no':
            latest_assets.cash_assets = False
    elif source == 'other_assets':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets = True
        elif answer == 'no':
            latest_assets.other_assets = False
    elif source == 'other_assets_receipt':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets_receipt = True
        elif answer == 'no':
            latest_assets.other_assets_receipt = False
    elif source == 'previous_year_net_wealth':
        show_success_message = True
        if answer == 'yes':
            latest_assets.previous_year_net_wealth = True
        elif answer == 'no':
            latest_assets.previous_year_net_wealth = False

    latest_assets.save()

    return show_success_message


def get_current_financial_year_agricultural_property_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return AgriculturalProperty.objects.filter(tax_payer_id=payer_id,
                                               financial_year_beg=financial_year_beg,
                                               financial_year_end=financial_year_end)


def get_current_financial_year_investments_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Investment.objects.filter(tax_payer_id=payer_id,
                                     financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end)


def get_current_financial_year_motor_vehicle_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return MotorVehicle.objects.filter(tax_payer_id=payer_id,
                                       financial_year_beg=financial_year_beg,
                                       financial_year_end=financial_year_end)
