from taxlover.services.income_service import get_total_other_income_taxable, get_total_allowed_amount, \
    get_current_financial_year_deduction_at_source_by_payer, get_current_financial_year_advance_tax_paid_by_payer, \
    get_current_financial_year_other_income_by_payer, get_current_financial_year_tax_rebate_by_payer, \
    get_current_financial_year_tax_refund_by_payer
from taxlover.services.salary_service import get_total_taxable, get_current_financial_year_salary_by_payer
from taxlover.utils import get_income_years, create_or_get_current_income_obj, get_gross_tax_before_tax_rebate


class IncomeDTO:

    def __init__(self, tax_payer_id, has_form_error):
        income = create_or_get_current_income_obj(tax_payer_id)
        salary = get_current_financial_year_salary_by_payer(tax_payer_id)
        other_income = get_current_financial_year_other_income_by_payer(tax_payer_id)
        tax_rebate = get_current_financial_year_tax_rebate_by_payer(tax_payer_id)
        tax_refund = get_current_financial_year_tax_refund_by_payer(tax_payer_id)

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

        self.income_year_beg, self.income_year_end = get_income_years()

        if salary:
            self.salaryId = salary.id
            self.total_salary_taxable = get_total_taxable(salary)
            self.total_salary_income = salary.get_total
            self.basic = salary.get_basic

        if other_income:
            self.otherIncomeId = other_income.id
            self.total_other_income_taxable = get_total_other_income_taxable(other_income)
            self.total_other_income = other_income.get_total
            self.total_exempted_other_income = self.total_other_income - self.total_other_income_taxable

        if tax_rebate:
            self.taxRebateId = tax_rebate.id
            self.total_invested_amount = tax_rebate.get_total
            self.total_allowed_amount = get_total_allowed_amount(tax_rebate)

        self.source_deductions = get_current_financial_year_deduction_at_source_by_payer(tax_payer_id)
        self.advance_tax_paid = get_current_financial_year_advance_tax_paid_by_payer(tax_payer_id)

        if tax_refund:
            self.taxRefundId = tax_refund.id
            self.tax_refund = tax_refund.get_refund

        self.has_form_error = has_form_error

        self.total_income = (self.total_salary_income if salary else 0) + \
                            (self.total_other_income if other_income else 0)

        self.total_taxable = (self.total_salary_taxable if salary else 0) + \
                            (self.total_other_income_taxable if other_income else 0)

        self.gross_tax_before_tax_rebate = get_gross_tax_before_tax_rebate(self.total_taxable)

