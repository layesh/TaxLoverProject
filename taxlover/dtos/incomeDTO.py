from taxlover.constants import INDIVIDUAL_TAX_PAYER_ONE_PAGE_TAXABLE_LIMIT, INDIVIDUAL_TAX_PAYER_INVESTMENT_MAX_LIMIT, \
    INDIVIDUAL_TAX_PAYER_INVESTMENT_RATE_ON_TAXABLE_AMOUNT
from taxlover.services.income_service import get_total_other_income_taxable, get_total_allowed_amount, \
    get_current_financial_year_deduction_at_source_by_payer, get_current_financial_year_advance_tax_paid_by_payer, \
    get_current_financial_year_other_income_by_payer, get_current_financial_year_tax_rebate_by_payer, \
    get_current_financial_year_tax_refund_by_payer, get_life_insurance_premium_allowed, get_contribution_to_dps_allowed
from taxlover.services.salary_service import get_total_taxable, get_current_financial_year_salary_by_payer, \
    get_current_financial_year_total_tax_deducted_at_source_by_payer, \
    get_current_financial_year_total_advance_tax_paid_by_payer, get_house_rent_exempted, get_medical_exempted, \
    get_conveyance_exempted
from taxlover.utils import get_income_years, create_or_get_current_income_obj, get_gross_tax_before_tax_rebate, \
    get_tax_rebate, get_net_tax_after_rebate, get_eligible_amount_of_investment_for_rebate, \
    get_total_rebate_on_taxable_income


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
            self.total_salary_exempted = self.total_salary_income - self.total_salary_taxable
            self.basic = salary.get_basic
            self.basic_exempted = 0
            self.basic_taxable = self.basic - self.basic_exempted
            self.house_rent = salary.get_house_rent
            self.house_rent_exempted = get_house_rent_exempted(salary.get_basic, salary.get_house_rent)
            self.house_rent_taxable = self.house_rent - self.house_rent_exempted
            self.medical = salary.get_medical
            self.medical_exempted = get_medical_exempted(salary.get_basic, salary.get_medical)
            self.medical_taxable = self.medical - self.medical_exempted
            self.conveyance = salary.get_conveyance
            self.conveyance_exempted = get_conveyance_exempted(salary.get_conveyance)
            self.conveyance_taxable = self.conveyance - self.conveyance_exempted
            self.lfa = salary.get_lfa
            self.lfa_exempted = salary.get_lfa
            self.lfa_taxable = 0
            self.other_allowances = salary.get_other_allowances
            self.other_allowances_exempted = 0
            self.other_allowances_taxable = salary.get_other_allowances
            self.bonus = salary.get_total_bonus
            self.bonus_exempted = 0
            self.bonus_taxable = salary.get_total_bonus
            self.employers_contribution_to_pf = salary.get_employers_contribution_to_pf
            self.employers_contribution_to_pf_exempted = 0
            self.employers_contribution_to_pf_taxable = salary.get_employers_contribution_to_pf

        if other_income:
            self.otherIncomeId = other_income.id
            self.total_other_income_taxable = get_total_other_income_taxable(other_income)
            self.total_other_income = other_income.get_total
            self.total_exempted_other_income = self.total_other_income - self.total_other_income_taxable

        if tax_rebate:
            self.taxRebateId = tax_rebate.id
            self.total_invested_amount = tax_rebate.get_total
            self.total_allowed_amount = get_total_allowed_amount(tax_rebate)
            self.life_insurance_premium_allowed = get_life_insurance_premium_allowed(tax_rebate.get_life_insurance_premium,
                                                                                     tax_rebate.get_life_insurance_premium_policy_value)
            self.contribution_to_dps_allowed = get_contribution_to_dps_allowed(tax_rebate.get_contribution_to_dps)
            self.investment_in_savings_certificates_sanchaypatra = tax_rebate.get_investment_in_savings_certificates_sanchaypatra
            self.investment_in_approved_debenture_or_stock_or_shares = tax_rebate.get_investment_in_approved_debenture_or_stock_or_shares
            self.contribution_to_pf_as_per_act_1925 = tax_rebate.get_contribution_to_pf_as_per_act_1925
            self.self_and_employers_contribution_to_pf = tax_rebate.get_self_and_employers_contribution_to_pf
            self.contribution_to_super_annuation_fund = tax_rebate.get_contribution_to_super_annuation_fund
            self.contribution_to_benevolent_fund_and_group_insurance_premium = tax_rebate.get_contribution_to_benevolent_fund_and_group_insurance_premium
            self.contribution_to_zakat_fund = tax_rebate.get_contribution_to_zakat_fund
            self.others_allowable_investment = tax_rebate.get_investment_in_bangladesh_govt_treasury_bond + \
                                               tax_rebate.get_donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation + \
                                               tax_rebate.get_donation_to_a_charitable_hospital_recognized_by_nbr + \
                                               tax_rebate.get_donation_to_organizations_set_up_for_the_welfare_of_retarded_people + \
                                               tax_rebate.get_contribution_to_national_level_institution_set_up_in_memory_of_liberation_war + \
                                               tax_rebate.get_contribution_to_liberation_war_museum + tax_rebate.get_contribution_to_aga_khan_development_network + \
                                               tax_rebate.get_contribution_to_asiatic_society_bangladesh + tax_rebate.get_donation_to_icddrb + \
                                               tax_rebate.get_donation_to_crp + tax_rebate.get_donation_to_educational_institution_recognized_by_government + \
                                               tax_rebate.get_contribution_to_ahsania_mission_cancer_hospital + tax_rebate.get_mutual_fund

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

        self.gross_tax_before_tax_rebate = get_gross_tax_before_tax_rebate(tax_payer_id, self.total_taxable)

        self.total_rebate_on_taxable_income = get_total_rebate_on_taxable_income(self.total_taxable)

        self.eligible_amount_of_investment_for_rebate = get_eligible_amount_of_investment_for_rebate(
            self.total_invested_amount if tax_rebate else 0, self.total_taxable)

        self.tax_rebate = get_tax_rebate(self.total_taxable, min(self.eligible_amount_of_investment_for_rebate,
                                                                 self.total_allowed_amount if tax_rebate else 0))

        self.net_tax_after_rebate = get_net_tax_after_rebate(self.gross_tax_before_tax_rebate,
                                                             self.tax_rebate)

        self.total_tax_deducted_at_source = get_current_financial_year_total_tax_deducted_at_source_by_payer(
            tax_payer_id)

        self.total_advance_tax = get_current_financial_year_total_advance_tax_paid_by_payer(
            tax_payer_id)

        self.tax_refund = tax_refund.get_refund if tax_refund else 0

        self.paid_with_return = self.net_tax_after_rebate - self.total_tax_deducted_at_source - \
                                self.total_advance_tax - self.tax_refund

        self.total_tax_paid = self.total_tax_deducted_at_source + self.total_advance_tax + self.tax_refund

        self.total_paid_and_adjusted = self.total_tax_deducted_at_source + self.total_advance_tax + self.tax_refund + \
                                       self.paid_with_return

        self.deficit = self.net_tax_after_rebate - self.total_paid_and_adjusted

        self.exempted_income = (self.total_salary_income - self.total_salary_taxable) if salary else 0

        self.eligible_for_one_page_return = True if self.total_taxable < INDIVIDUAL_TAX_PAYER_ONE_PAGE_TAXABLE_LIMIT \
            else False

        self.investment_max_limit = INDIVIDUAL_TAX_PAYER_INVESTMENT_MAX_LIMIT

        self.investment_rate_on_taxable_amount = INDIVIDUAL_TAX_PAYER_INVESTMENT_RATE_ON_TAXABLE_AMOUNT * 100


