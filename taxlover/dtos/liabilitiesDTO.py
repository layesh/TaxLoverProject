from taxlover.services.assets_service import get_current_financial_year_agricultural_property_by_payer, \
    get_current_financial_year_investments_by_payer, get_current_financial_year_motor_vehicle_by_payer, \
    get_current_financial_year_furniture_by_payer, get_current_financial_year_jewellery_by_payer, \
    get_current_financial_year_electronic_equipment_by_payer, get_current_financial_year_other_assets_by_payer, \
    get_current_financial_year_other_assets_receipt_by_payer, get_current_financial_year_cash_assets_by_payer, \
    get_current_financial_year_previous_year_net_wealth_by_payer
from taxlover.services.liabilities_service import get_current_financial_year_unsecured_loans_by_payer, \
    get_current_financial_year_other_liabilities_by_payer, get_current_financial_year_bank_loans_by_payer, \
    get_current_financial_year_mortgages_by_payer
from taxlover.utils import get_income_years, create_or_get_current_assets_obj, create_or_get_current_liabilities_obj


class LiabilitiesDTO:

    def __init__(self, tax_payer_id, has_form_error):
        liabilities = create_or_get_current_liabilities_obj(tax_payer_id)

        self.has_mortgages = liabilities.has_mortgages
        self.has_no_mortgages = liabilities.has_no_mortgages
        self.has_unsecured_loans = liabilities.has_unsecured_loans
        self.has_no_unsecured_loans = liabilities.has_no_unsecured_loans
        self.has_bank_loans = liabilities.has_bank_loans
        self.has_no_bank_loans = liabilities.has_no_bank_loans
        self.has_other_liabilities = liabilities.has_other_liabilities
        self.has_no_other_liabilities = liabilities.has_no_other_liabilities

        self.income_year_beg, self.income_year_end = get_income_years()

        self.mortgages = get_current_financial_year_mortgages_by_payer(tax_payer_id)
        self.unsecured_loans = get_current_financial_year_unsecured_loans_by_payer(tax_payer_id)
        self.bank_loans = get_current_financial_year_bank_loans_by_payer(tax_payer_id)
        self.other_liabilities = get_current_financial_year_other_liabilities_by_payer(tax_payer_id)

        self.has_form_error = has_form_error

