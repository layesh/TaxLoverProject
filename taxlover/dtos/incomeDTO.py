from taxlover.services.salary_service import get_total_taxable
from taxlover.utils import get_income_years


class IncomeDTO:

    def __init__(self, income, salary):
        self.has_salary_income = income.has_salary_income
        self.has_no_salary_income = income.has_no_salary_income
        self.has_interest_on_securities = income.has_interest_on_securities
        self.has_no_interest_on_securities = income.has_no_interest_on_securities
        self.has_rental_property = income.has_rental_property
        self.has_no_rental_property = income.has_no_rental_property
        self.has_agriculture = income.has_agriculture
        self.has_no_agriculture = income.has_no_agriculture
        self.has_business = income.has_business
        self.has_no_business = income.has_no_business
        self.has_share_of_profit_in_firm = income.has_share_of_profit_in_firm
        self.has_no_share_of_profit_in_firm = income.has_no_share_of_profit_in_firm
        self.has_spouse_or_child = income.has_spouse_or_child
        self.has_no_spouse_or_child = income.has_no_spouse_or_child
        self.has_capital_gains = income.has_capital_gains
        self.has_no_capital_gains = income.has_no_capital_gains
        self.has_other_sources = income.has_other_sources
        self.has_no_other_sources = income.has_no_other_sources
        self.has_foreign_income = income.has_foreign_income
        self.has_no_foreign_income = income.has_no_foreign_income
        self.has_tax_rebate = income.has_tax_rebate
        self.has_no_tax_rebate = income.has_no_tax_rebate
        self.has_tax_deducted_at_source = income.has_tax_deducted_at_source
        self.has_no_tax_deducted_at_source = income.has_no_tax_deducted_at_source
        self.has_advance_paid_tax = income.has_advance_paid_tax
        self.has_no_advance_paid_tax = income.has_no_advance_paid_tax
        self.has_adjustment_of_tax_refund = income.has_adjustment_of_tax_refund
        self.has_no_adjustment_of_tax_refund = income.has_no_adjustment_of_tax_refund
        if salary:
            self.income_year_beg, self.income_year_end = get_income_years()
            self.salaryId = salary.id
            self.taxable = get_total_taxable(salary)
            self.total = salary.get_total
            self.basic = salary.get_basic
