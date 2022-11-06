from taxlover.services.assets_service import get_agricultural_property_by_payer, \
    get_investments_by_payer, get_motor_vehicle_by_payer, \
    get_furniture_by_payer, get_jewellery_by_payer, \
    get_electronic_equipment_by_payer, get_other_assets_by_payer, \
    get_other_assets_receipt_by_payer, get_cash_assets_by_payer, \
    get_net_wealth_by_payer
from taxlover.services.liabilities_service import get_unsecured_loans_by_payer, \
    get_other_liabilities_by_payer, get_bank_loans_by_payer, \
    get_mortgages_by_payer, get_total_unsecured_loans_value, get_total_other_liabilities_value, \
    get_total_mortgage_and_bank_loan_value
from taxlover.utils import get_income_years, create_or_get_assets_obj, create_or_get_liabilities_obj


class LiabilitiesDTO:

    def __init__(self, tax_payer_id, has_form_error, previous_year=None):
        liabilities = create_or_get_liabilities_obj(tax_payer_id, True, previous_year)

        self.has_mortgages = liabilities.has_mortgages
        self.has_no_mortgages = liabilities.has_no_mortgages
        self.has_unsecured_loans = liabilities.has_unsecured_loans
        self.has_no_unsecured_loans = liabilities.has_no_unsecured_loans
        self.has_bank_loans = liabilities.has_bank_loans
        self.has_no_bank_loans = liabilities.has_no_bank_loans
        self.has_other_liabilities = liabilities.has_other_liabilities
        self.has_no_other_liabilities = liabilities.has_no_other_liabilities

        self.income_year_beg, self.income_year_end = get_income_years()

        self.mortgages = get_mortgages_by_payer(tax_payer_id, previous_year)
        self.unsecured_loans = get_unsecured_loans_by_payer(tax_payer_id, previous_year)
        self.bank_loans = get_bank_loans_by_payer(tax_payer_id, previous_year)
        self.other_liabilities = get_other_liabilities_by_payer(tax_payer_id, previous_year)

        self.total_unsecured_loans_value = get_total_unsecured_loans_value(self.unsecured_loans)
        self.total_mortgage_and_bank_loan_value = get_total_mortgage_and_bank_loan_value(self.mortgages, self.bank_loans)
        self.total_other_liabilities_value = get_total_other_liabilities_value(self.other_liabilities)

        self.total_liabilities = self.total_unsecured_loans_value + self.total_mortgage_and_bank_loan_value + self.total_other_liabilities_value

        self.has_form_error = has_form_error

