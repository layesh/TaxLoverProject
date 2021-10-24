from taxlover.models import AgriculturalProperty, Investment, MotorVehicle, Furniture, Jewellery, ElectronicEquipment, \
    CashAssets, OtherAssets, OtherAssetsReceipt, PreviousYearNetWealth
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
            furnitures = get_current_financial_year_furniture_by_payer(request.user.id)
            if furnitures:
                furnitures.delete()
    elif source == 'jewellery':
        show_success_message = True
        if answer == 'yes':
            latest_assets.jewellery = True
        elif answer == 'no':
            latest_assets.jewellery = False
            jewelleries = get_current_financial_year_jewellery_by_payer(request.user.id)
            if jewelleries:
                jewelleries.delete()
    elif source == 'electronic_equipment':
        show_success_message = True
        if answer == 'yes':
            latest_assets.electronic_equipment = True
        elif answer == 'no':
            latest_assets.electronic_equipment = False
            equipments = get_current_financial_year_electronic_equipment_by_payer(request.user.id)
            if equipments:
                equipments.delete()
    elif source == 'cash_assets':
        if answer == 'yes':
            latest_assets.cash_assets = True
        elif answer == 'no':
            show_success_message = True
            latest_assets.cash_assets = False
            cash_assets = get_current_financial_year_cash_assets_by_payer(request.user.id)
            if cash_assets:
                cash_assets.delete()
    elif source == 'other_assets':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets = True
        elif answer == 'no':
            latest_assets.other_assets = False
            other_assets = get_current_financial_year_other_assets_by_payer(request.user.id)
            if other_assets:
                other_assets.delete()
    elif source == 'other_assets_receipt':
        show_success_message = True
        if answer == 'yes':
            latest_assets.other_assets_receipt = True
        elif answer == 'no':
            latest_assets.other_assets_receipt = False
            other_assets_receipt = get_current_financial_year_other_assets_receipt_by_payer(request.user.id)
            if other_assets_receipt:
                other_assets_receipt.delete()
    elif source == 'previous_year_net_wealth':
        show_success_message = True
        if answer == 'yes':
            latest_assets.previous_year_net_wealth = True
        elif answer == 'no':
            latest_assets.previous_year_net_wealth = False
            previous_year_net_wealth = get_current_financial_year_previous_year_net_wealth_by_payer(request.user.id)
            if previous_year_net_wealth:
                previous_year_net_wealth.delete()

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


def get_current_financial_year_furniture_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Furniture.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end)


def get_current_financial_year_jewellery_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Jewellery.objects.filter(tax_payer_id=payer_id,
                                    financial_year_beg=financial_year_beg,
                                    financial_year_end=financial_year_end)


def get_current_financial_year_electronic_equipment_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return ElectronicEquipment.objects.filter(tax_payer_id=payer_id,
                                              financial_year_beg=financial_year_beg,
                                              financial_year_end=financial_year_end)


def get_current_financial_year_cash_assets_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return CashAssets.objects.filter(tax_payer_id=payer_id,
                                     financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end).first()


def get_current_financial_year_other_assets_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return OtherAssets.objects.filter(tax_payer_id=payer_id,
                                      financial_year_beg=financial_year_beg,
                                      financial_year_end=financial_year_end)


def get_current_financial_year_other_assets_receipt_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return OtherAssetsReceipt.objects.filter(tax_payer_id=payer_id,
                                             financial_year_beg=financial_year_beg,
                                             financial_year_end=financial_year_end)


def get_current_financial_year_previous_year_net_wealth_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return PreviousYearNetWealth.objects.filter(tax_payer_id=payer_id,
                                                financial_year_beg=financial_year_beg,
                                                financial_year_end=financial_year_end).first()
