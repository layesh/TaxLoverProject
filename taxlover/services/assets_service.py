from django.db.models import Sum

from taxlover.models import AgriculturalProperty, Investment, MotorVehicle, Furniture, Jewellery, ElectronicEquipment, \
    CashAssets, OtherAssets, OtherAssetsReceipt, PreviousYearNetWealth, Assets, Liabilities
from taxlover.utils import get_income_years, get_previous_income_years


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
            investments = get_investments_by_payer(request.user.id)
            if investments:
                investments.delete()
    elif source == 'motor_vehicle':
        if answer == 'yes':
            latest_assets.motor_vehicle = True
        elif answer == 'no':
            show_success_message = True
            latest_assets.motor_vehicle = False
            investments = get_motor_vehicle_by_payer(request.user.id)
            if investments:
                investments.delete()
    elif source == 'furniture':
        show_success_message = True
        if answer == 'yes':
            latest_assets.furniture = True
        elif answer == 'no':
            latest_assets.furniture = False
            furnitures = get_furniture_by_payer(request.user.id)
            if furnitures:
                furnitures.delete()
    elif source == 'jewellery':
        show_success_message = True
        if answer == 'yes':
            latest_assets.jewellery = True
        elif answer == 'no':
            latest_assets.jewellery = False
            jewelleries = get_jewellery_by_payer(request.user.id)
            if jewelleries:
                jewelleries.delete()
    elif source == 'electronic_equipment':
        show_success_message = True
        if answer == 'yes':
            latest_assets.electronic_equipment = True
        elif answer == 'no':
            latest_assets.electronic_equipment = False
            equipments = get_electronic_equipment_by_payer(request.user.id)
            if equipments:
                equipments.delete()
    elif source == 'cash_assets':
        if answer == 'yes':
            latest_assets.cash_assets = True
        elif answer == 'no':
            show_success_message = True
            latest_assets.cash_assets = False
            cash_assets = get_cash_assets_by_payer(request.user.id)
            if cash_assets:
                cash_assets.delete()
    elif source == 'other_assets':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets = True
        elif answer == 'no':
            latest_assets.other_assets = False
            other_assets = get_other_assets_by_payer(request.user.id)
            if other_assets:
                other_assets.delete()
    elif source == 'other_assets_receipt':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets_receipt = True
        elif answer == 'no':
            latest_assets.other_assets_receipt = False
            other_assets_receipt = get_other_assets_receipt_by_payer(request.user.id)
            if other_assets_receipt:
                other_assets_receipt.delete()
    elif source == 'previous_year_net_wealth':
        show_success_message = True
        if answer == 'yes':
            latest_assets.previous_year_net_wealth = True
        elif answer == 'no':
            latest_assets.previous_year_net_wealth = False
            previous_year_net_wealth = get_net_wealth_by_payer(request.user.id)
            if previous_year_net_wealth:
                previous_year_net_wealth.delete()

    latest_assets.save()

    return show_success_message


def get_agricultural_property_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return AgriculturalProperty.objects.filter(tax_payer_id=payer_id,
                                               financial_year_beg=financial_year_beg,
                                               financial_year_end=financial_year_end)


def get_total_agricultural_property_value(agricultural_properties):
    total = agricultural_properties.aggregate(Sum('property_value'))

    return total['property_value__sum'] if total['property_value__sum'] is not None else 0


def get_investments_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return Investment.objects.filter(tax_payer_id=payer_id,
                                     financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end)


def get_total_investment_value(investments):
    total = investments.aggregate(Sum('value'))

    return total['value__sum'] if total['value__sum'] is not None else 0


def get_total_investment_value_by_type(investments, investment_type):
    total = investments.filter(type=investment_type).aggregate(Sum('value'))

    return total['value__sum'] if total['value__sum'] is not None else 0


def get_motor_vehicle_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return MotorVehicle.objects.filter(tax_payer_id=payer_id,
                                       financial_year_beg=financial_year_beg,
                                       financial_year_end=financial_year_end)


def get_furniture_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return Furniture.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end)


def get_jewellery_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return Jewellery.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end)


def get_total_jewellery_value(jewelleries):
    total = jewelleries.aggregate(Sum('jewellery_value'))

    return total['jewellery_value__sum'] if total['jewellery_value__sum'] is not None else 0


def get_electronic_equipment_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return ElectronicEquipment.objects.filter(tax_payer_id=payer_id,
                                              financial_year_beg=financial_year_beg,
                                              financial_year_end=financial_year_end)


def get_total_furniture_and_electronic_items_value(furnitures, electronic_equipments):
    total_furniture_value = furnitures.aggregate(Sum('furniture_value'))
    total_electronic_equipments_value = electronic_equipments.aggregate(Sum('equipment_value'))

    total_value = (total_furniture_value['furniture_value__sum'] if total_furniture_value['furniture_value__sum'] is not None else 0) + \
                  (total_electronic_equipments_value['equipment_value__sum'] if total_electronic_equipments_value['equipment_value__sum'] is not None else 0)

    return total_value


def get_cash_assets_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return CashAssets.objects.filter(tax_payer_id=payer_id,
                                     financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end).first()


def get_other_assets_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return OtherAssets.objects.filter(tax_payer_id=payer_id,
                                      financial_year_beg=financial_year_beg,
                                      financial_year_end=financial_year_end)


def get_other_assets_receipt_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return OtherAssetsReceipt.objects.filter(tax_payer_id=payer_id,
                                             financial_year_beg=financial_year_beg,
                                             financial_year_end=financial_year_end)


def get_total_other_asset_value(other_assets, other_assets_receipt):
    total_other_asset_value = other_assets.aggregate(Sum('asset_value'))
    total_other_assets_receipt_value = other_assets_receipt.aggregate(Sum('other_asset_value'))

    total_value = (total_other_asset_value['asset_value__sum'] if total_other_asset_value['asset_value__sum'] is not None else 0) + \
                  (total_other_assets_receipt_value['other_asset_value__sum'] if total_other_assets_receipt_value['other_asset_value__sum'] is not None else 0)

    return total_value


def get_net_wealth_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return PreviousYearNetWealth.objects.filter(tax_payer_id=payer_id,
                                                financial_year_beg=financial_year_beg,
                                                financial_year_end=financial_year_end).first()


def copy_assets_data_from_previous_year(payer_id):
    previous_income_year_beg, previous_income_year_end = get_previous_income_years()

    prev_year_asset = Assets.objects.get(tax_payer_id=payer_id, income_year_beg=previous_income_year_beg,
                                         income_year_end=previous_income_year_end)

    income_year_beg, income_year_end = get_income_years()
    prev_year_asset.id = None
    prev_year_asset.income_year_beg = income_year_beg
    prev_year_asset.income_year_end = income_year_end

    prev_year_asset.save()

    agricultural_properties = get_agricultural_property_by_payer(payer_id, True)
    investments = get_investments_by_payer(payer_id, True)
    motor_vehicles = get_motor_vehicle_by_payer(payer_id, True)
    furnitures = get_furniture_by_payer(payer_id, True)
    jewelleries = get_jewellery_by_payer(payer_id, True)
    electronic_equipments = get_electronic_equipment_by_payer(payer_id, True)
    other_assets = get_other_assets_by_payer(payer_id, True)
    other_assets_receipts = get_other_assets_receipt_by_payer(payer_id, True)
    cash_assets = get_cash_assets_by_payer(payer_id, True)
    previous_year_net_wealth = get_net_wealth_by_payer(payer_id, True)

    for asset in agricultural_properties:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in investments:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in motor_vehicles:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in furnitures:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in jewelleries:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in electronic_equipments:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in other_assets:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    for asset in other_assets_receipts:
        asset.id = None
        asset.financial_year_beg = income_year_beg
        asset.financial_year_end = income_year_end
        asset.save()

    if cash_assets:
        cash_assets.id = None
        cash_assets.financial_year_beg = income_year_beg
        cash_assets.financial_year_end = income_year_end
        cash_assets.save()

    if previous_year_net_wealth:
        previous_year_net_wealth.id = None
        previous_year_net_wealth.financial_year_beg = income_year_beg
        previous_year_net_wealth.financial_year_end = income_year_end
        previous_year_net_wealth.save()
