from taxlover.dtos.assetsDTO import AssetsDTO
from taxlover.dtos.liabilitiesDTO import LiabilitiesDTO
from taxlover.models import Assets
from taxlover.services.assets_service import get_agricultural_property_by_payer, get_investments_by_payer, \
    get_motor_vehicle_by_payer, get_furniture_by_payer, get_jewellery_by_payer, get_electronic_equipment_by_payer, \
    get_other_assets_by_payer, get_other_assets_receipt_by_payer, get_cash_assets_by_payer, get_net_wealth_by_payer
from taxlover.utils import get_previous_income_years, get_income_years


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
        asset_dto = AssetsDTO(payer_id, False, True)
        liabilities_dto = LiabilitiesDTO(payer_id, False, True)
        net_wealth = asset_dto.gross_wealth - liabilities_dto.total_liabilities
        previous_year_net_wealth.wealth_value = net_wealth
        previous_year_net_wealth.save()
