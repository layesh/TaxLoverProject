from taxlover.services.assets_service import get_current_financial_year_agricultural_property_by_payer
from taxlover.services.income_service import get_total_other_income_taxable, get_total_allowed_amount, \
    get_current_financial_year_deduction_at_source_by_payer, get_current_financial_year_advance_tax_paid_by_payer, \
    get_current_financial_year_other_income_by_payer, get_current_financial_year_tax_rebate_by_payer, \
    get_current_financial_year_tax_refund_by_payer
from taxlover.services.salary_service import get_total_taxable, get_current_financial_year_salary_by_payer
from taxlover.utils import get_income_years, create_or_get_current_income_obj, create_or_get_current_assets_obj


class AssetsDTO:

    def __init__(self, tax_payer_id, has_form_error):
        assets = create_or_get_current_assets_obj(tax_payer_id)

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

        self.has_form_error = has_form_error

