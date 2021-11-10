from taxlover.models import INVESTMENT_TYPE
from taxlover.services.assets_service import get_current_financial_year_agricultural_property_by_payer, \
    get_current_financial_year_investments_by_payer, get_current_financial_year_motor_vehicle_by_payer, \
    get_current_financial_year_furniture_by_payer, get_current_financial_year_jewellery_by_payer, \
    get_current_financial_year_electronic_equipment_by_payer, get_current_financial_year_other_assets_by_payer, \
    get_current_financial_year_other_assets_receipt_by_payer, get_current_financial_year_cash_assets_by_payer, \
    get_current_financial_year_previous_year_net_wealth_by_payer, get_total_agricultural_property_value, \
    get_total_investment_value, get_total_investment_value_by_type, get_total_jewellery_value, \
    get_total_furniture_and_electronic_items_value, get_total_other_asset_value
from taxlover.utils import get_income_years, create_or_get_current_assets_obj


class AssetsDTO:

    def __init__(self, tax_payer_id, has_form_error):
        assets = create_or_get_current_assets_obj(tax_payer_id)
        cash_assets = get_current_financial_year_cash_assets_by_payer(tax_payer_id)
        self.previous_year_net_wealth = get_current_financial_year_previous_year_net_wealth_by_payer(tax_payer_id)

        self.has_business_capital = assets.has_business_capital
        self.has_no_business_capital = assets.has_no_business_capital
        self.has_directors_shareholding_assets = assets.has_directors_shareholding_assets
        self.has_no_directors_shareholding_assets = assets.has_no_directors_shareholding_assets
        self.has_non_agricultural_property = assets.has_non_agricultural_property
        self.has_no_non_agricultural_property = assets.has_no_non_agricultural_property
        self.has_agricultural_property = assets.has_agricultural_property
        self.has_no_agricultural_property = assets.has_no_agricultural_property
        self.has_investments = assets.has_investments
        self.has_no_investments = assets.has_no_investments
        self.has_motor_vehicle = assets.has_motor_vehicle
        self.has_no_motor_vehicle = assets.has_no_motor_vehicle
        self.has_furniture = assets.has_furniture
        self.has_no_furniture = assets.has_no_furniture
        self.has_jewellery = assets.has_jewellery
        self.has_no_jewellery = assets.has_no_jewellery
        self.has_electronic_equipment = assets.has_electronic_equipment
        self.has_no_electronic_equipment = assets.has_no_electronic_equipment
        self.has_cash_assets = assets.has_cash_assets
        self.has_no_cash_assets = assets.has_no_cash_assets
        self.has_other_assets = assets.has_other_assets
        self.has_no_other_assets = assets.has_no_other_assets
        self.has_other_assets_receipt = assets.has_other_assets_receipt
        self.has_no_other_assets_receipt = assets.has_no_other_assets_receipt
        self.has_previous_year_net_wealth = assets.has_previous_year_net_wealth
        self.has_no_previous_year_net_wealth = assets.has_no_previous_year_net_wealth

        self.income_year_beg, self.income_year_end = get_income_years()

        self.agricultural_properties = get_current_financial_year_agricultural_property_by_payer(tax_payer_id)
        self.total_agricultural_properties_value = get_total_agricultural_property_value(self.agricultural_properties)
        self.investments = get_current_financial_year_investments_by_payer(tax_payer_id)
        self.total_investment_value = get_total_investment_value(self.investments)
        self.total_shares_debentures_investment_value = get_total_investment_value_by_type(self.investments,
                                                                                           'Shares/Debentures')
        self.total_saving_cert_investment_value = get_total_investment_value_by_type(self.investments,
                                                                                           'Saving Certificate/Unit Certificate/Bond')
        self.total_saving_scheme_investment_value = get_total_investment_value_by_type(self.investments,
                                                                                           'Prize Bond/Saving Scheme/FDR/DPS')
        self.total_loans_given_investment_value = get_total_investment_value_by_type(self.investments,
                                                                                           'Loans Given')
        self.total_other_investment_investment_value = get_total_investment_value_by_type(self.investments,
                                                                                           'Other Investment')
        self.motor_vehicles = get_current_financial_year_motor_vehicle_by_payer(tax_payer_id)

        total_motor_vehicle_value = 0

        if self.motor_vehicles.count() > 0:
            self.motor_vehicles_01 = self.motor_vehicles[0]
            total_motor_vehicle_value += self.motor_vehicles_01.get_value
        if self.motor_vehicles.count() > 1:
            self.motor_vehicles_02 = self.motor_vehicles[1]
            total_motor_vehicle_value += self.motor_vehicles_02.get_value

        self.furnitures = get_current_financial_year_furniture_by_payer(tax_payer_id)
        self.jewelleries = get_current_financial_year_jewellery_by_payer(tax_payer_id)
        self.total_jewellery_value = get_total_jewellery_value(self.jewelleries)
        self.electronic_equipments = get_current_financial_year_electronic_equipment_by_payer(tax_payer_id)
        self.total_furniture_and_electronic_items_value = get_total_furniture_and_electronic_items_value(
            self.furnitures, self.electronic_equipments)
        self.other_assets = get_current_financial_year_other_assets_by_payer(tax_payer_id)
        self.other_assets_receipts = get_current_financial_year_other_assets_receipt_by_payer(tax_payer_id)
        self.total_other_asset_value = get_total_other_asset_value(self.other_assets, self.other_assets_receipts)

        if cash_assets:
            self.cashAssetsId = cash_assets.id
            self.cash_in_hand = cash_assets.get_cash_in_hand
            self.cash_at_bank = cash_assets.get_cash_at_bank
            self.other_fund = cash_assets.get_other_fund
            self.other_deposits = cash_assets.get_other_deposits
            self.total_cash_assets = self.cash_in_hand + self.cash_at_bank + self.other_fund + self.other_deposits

        if self.previous_year_net_wealth:
            self.previousYearNetWealthId = self.previous_year_net_wealth.id
            self.previous_year_net_wealth_value = self.previous_year_net_wealth.wealth_value

        self.has_form_error = has_form_error

        self.gross_wealth = self.total_agricultural_properties_value + self.total_investment_value + \
                            total_motor_vehicle_value + self.total_jewellery_value + \
                            self.total_furniture_and_electronic_items_value + self.total_other_asset_value + \
                            self.total_cash_assets if cash_assets else 0

