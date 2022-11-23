import os
from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

from TaxLoverProject import settings


class Division(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GenderChoices(Enum):
    M = 'Male'
    F = 'Female'
    T = 'Transgender'


class TaxPayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, null=True)
    e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    dob = models.DateField(blank=True, null=True)
    married = models.BooleanField(null=True)
    spouse_name = models.CharField(max_length=250, null=True)
    spouse_e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    has_differently_abled_children = models.BooleanField(null=True)
    gender = models.CharField(max_length=1, choices=[(tag, tag.value) for tag in GenderChoices], null=True)
    resident = models.BooleanField(null=True)
    nid = models.CharField(max_length=17, null=True)
    differently_abled = models.BooleanField(null=True)
    fathers_name = models.CharField(max_length=250, null=True)
    mothers_name = models.CharField(max_length=250, null=True)
    num_of_dependent_adult = models.IntegerField(null=True)
    num_of_dependent_child = models.IntegerField(null=True)
    gazetted_war_wounded_freedom_fighter = models.BooleanField(null=True)
    government_employee = models.BooleanField(null=True)
    RESIDENCE_AREA = (
        (1, 'Dhaka and Chittagong City Corporation'),
        (2, 'Other City Corporation'),
        (3, 'Other Areas')
    )
    residence_area = models.IntegerField(choices=RESIDENCE_AREA, null=True)
    tax_zone = models.IntegerField(null=True)
    tax_circle = models.IntegerField(null=True)
    employer_name = models.CharField(max_length=250, null=True)
    employer_address = models.CharField(max_length=250, null=True)
    employer_bin = models.CharField(max_length=20, null=True)
    present_address_line_one = models.CharField(max_length=250, null=True)
    present_address_line_two = models.CharField(max_length=250, null=True)
    present_address_postcode = models.IntegerField(null=True)
    present_address_division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    present_address_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    same_address = models.BooleanField(null=True)
    permanent_address = models.CharField(max_length=250, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    aged_65_years_or_more = models.BooleanField(null=True)

    def __str__(self):
        return self.name

    @property
    def get_e_tin(self):
        if self.e_tin:
            return self.e_tin
        else:
            return ""

    @property
    def get_spouse_e_tin(self):
        if self.spouse_e_tin:
            return self.spouse_e_tin
        else:
            return ""

    @property
    def get_nid(self):
        if self.nid:
            return self.nid
        else:
            return ""

    @property
    def get_dob(self):
        if self.dob:
            try:
                return self.dob.strftime("%d/%m/%Y")
            except AttributeError:
                return self.dob
        else:
            return ""

    @property
    def get_contact_no(self):
        if self.mobile_no:
            return self.mobile_no
        else:
            return ""

    @property
    def get_tax_circle(self):
        if self.tax_circle:
            return self.tax_circle
        else:
            return ""

    @property
    def get_tax_zone(self):
        if self.tax_zone:
            return self.tax_zone
        else:
            return ""

    @property
    def is_resident(self):
        if self.resident is not None:
            if self.resident:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_non_resident(self):
        if self.resident is not None:
            if self.resident:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def get_name(self):
        if self.name:
            return self.name
        else:
            return ""

    @property
    def get_spouse_name(self):
        if self.spouse_name:
            return self.spouse_name
        else:
            return ""

    @property
    def is_single(self):
        if self.married is not None:
            if self.married:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def is_married(self):
        if self.married is not None:
            if self.married:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def get_fathers_name(self):
        if self.fathers_name:
            return self.fathers_name
        else:
            return ""

    @property
    def get_mothers_name(self):
        if self.mothers_name:
            return self.mothers_name
        else:
            return ""

    @property
    def get_present_address_line_one(self):
        if self.present_address_line_one:
            return self.present_address_line_one
        else:
            return ""

    @property
    def get_permanent_address(self):
        if self.permanent_address:
            return self.permanent_address
        else:
            return ""

    @property
    def get_email(self):
        if self.email:
            return self.email
        else:
            return ""

    @property
    def is_male(self):
        if self.gender is not None:
            if self.gender and self.gender == GenderChoices.M.name:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_female(self):
        if self.gender is not None:
            if self.gender and self.gender == GenderChoices.F.name:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def get_employer_name(self):
        if self.employer_name:
            return self.employer_name
        else:
            return ""

    @property
    def is_gazetted_war_wounded_freedom_fighter(self):
        if self.gazetted_war_wounded_freedom_fighter is not None:
            if self.gazetted_war_wounded_freedom_fighter:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_differently_abled(self):
        if self.differently_abled is not None:
            if self.differently_abled:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_aged_65_years_or_more(self):
        if self.aged_65_years_or_more is not None:
            if self.aged_65_years_or_more:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_has_differently_abled_children(self):
        if self.has_differently_abled_children is not None:
            if self.has_differently_abled_children:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_government_employee(self):
        if self.government_employee is not None:
            if self.government_employee:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def is_non_government_employee(self):
        if self.government_employee is not None:
            if self.government_employee:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def get_bin(self):
        if self.employer_bin:
            return self.employer_bin
        else:
            return ""


class Salary(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    basic = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    house_rent = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    medical = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    conveyance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    lfa = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    festival_bonus = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_bonus = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total_bonus = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    employers_contribution_to_pf = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    employees_contribution_to_pf = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    ait = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    special_pay = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    dearness_allowance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    support_staff_allowance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    leave_encashment = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    honorarium_or_reward = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    overtime_allowance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_allowances = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    interest_accrued_from_pf = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    deemed_income_transport = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    deemed_free_accommodation = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    bengali_new_year_bonus = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    festival_allowance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pension = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    income_from_pf_and_saf = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    others = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    arrear_pay = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.tax_payer.name} Salary'

    def get_absolute_url(self):
        return reverse('salary-detail', kwargs={'pk': self.pk})

    @property
    def get_basic(self):
        if self.basic:
            return self.basic
        else:
            return 0

    @property
    def get_house_rent(self):
        if self.house_rent:
            return self.house_rent
        else:
            return 0

    @property
    def get_medical(self):
        if self.medical:
            return self.medical
        else:
            return 0

    @property
    def get_conveyance(self):
        if self.conveyance:
            return self.conveyance
        else:
            return 0

    @property
    def get_lfa(self):
        if self.lfa:
            return self.lfa
        else:
            return 0

    @property
    def get_other_allowances(self):
        if self.other_allowances:
            return self.other_allowances
        else:
            return 0

    @property
    def get_total_bonus(self):
        if self.total_bonus:
            return self.total_bonus
        else:
            return 0

    @property
    def get_employers_contribution_to_pf(self):
        if self.employers_contribution_to_pf:
            return self.employers_contribution_to_pf
        else:
            return 0

    @property
    def get_total(self):
        return self.get_basic + self.get_house_rent + self.get_medical + self.get_conveyance + self.get_lfa + \
               + self.get_other_allowances + self.get_total_bonus + self.get_employers_contribution_to_pf


class Income(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    salary = models.BooleanField(null=True)
    interest_on_security = models.BooleanField(null=True)
    rental_property = models.BooleanField(null=True)
    agriculture = models.BooleanField(null=True)
    business = models.BooleanField(null=True)
    share_of_profit_in_firm = models.BooleanField(null=True)
    spouse_or_child = models.BooleanField(null=True)
    capital_gains = models.BooleanField(null=True)
    other_sources = models.BooleanField(null=True)
    foreign_income = models.BooleanField(null=True)
    tax_rebate = models.BooleanField(null=True)
    tax_deducted_at_source = models.BooleanField(null=True)
    advance_paid_tax = models.BooleanField(null=True)
    adjustment_of_tax_refund = models.BooleanField(null=True)
    income_year_beg = models.IntegerField(default=0)
    income_year_end = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.tax_payer.name} Income'

    @property
    def has_salary_income(self):
        if self.salary is not None:
            if self.salary:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_salary_income(self):
        if self.salary is not None:
            if self.salary:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_interest_on_securities(self):
        if self.interest_on_security is not None:
            if self.interest_on_security:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_interest_on_securities(self):
        if self.interest_on_security is not None:
            if self.interest_on_security:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_rental_property(self):
        if self.rental_property is not None:
            if self.rental_property:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_rental_property(self):
        if self.rental_property is not None:
            if self.rental_property:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_agriculture(self):
        if self.agriculture is not None:
            if self.agriculture:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_agriculture(self):
        if self.agriculture is not None:
            if self.agriculture:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_business(self):
        if self.business is not None:
            if self.business:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_business(self):
        if self.business is not None:
            if self.business:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_share_of_profit_in_firm(self):
        if self.share_of_profit_in_firm is not None:
            if self.share_of_profit_in_firm:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_share_of_profit_in_firm(self):
        if self.share_of_profit_in_firm is not None:
            if self.share_of_profit_in_firm:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_spouse_or_child(self):
        if self.spouse_or_child is not None:
            if self.spouse_or_child:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_spouse_or_child(self):
        if self.spouse_or_child is not None:
            if self.spouse_or_child:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_capital_gains(self):
        if self.capital_gains is not None:
            if self.capital_gains:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_capital_gains(self):
        if self.capital_gains is not None:
            if self.capital_gains:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_other_sources(self):
        if self.other_sources is not None:
            if self.other_sources:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_other_sources(self):
        if self.other_sources is not None:
            if self.other_sources:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_foreign_income(self):
        if self.foreign_income is not None:
            if self.foreign_income:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_foreign_income(self):
        if self.foreign_income is not None:
            if self.foreign_income:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_tax_rebate(self):
        if self.tax_rebate is not None:
            if self.tax_rebate:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_tax_rebate(self):
        if self.tax_rebate is not None:
            if self.tax_rebate:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_tax_deducted_at_source(self):
        if self.tax_deducted_at_source is not None:
            if self.tax_deducted_at_source:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_tax_deducted_at_source(self):
        if self.tax_deducted_at_source is not None:
            if self.tax_deducted_at_source:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_advance_paid_tax(self):
        if self.advance_paid_tax is not None:
            if self.advance_paid_tax:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_advance_paid_tax(self):
        if self.advance_paid_tax is not None:
            if self.advance_paid_tax:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_adjustment_of_tax_refund(self):
        if self.adjustment_of_tax_refund is not None:
            if self.adjustment_of_tax_refund:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_adjustment_of_tax_refund(self):
        if self.adjustment_of_tax_refund is not None:
            if self.adjustment_of_tax_refund:
                return ""
            else:
                return "checked"
        else:
            return ""


class Document(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, null=True)
    income_year_beg = models.IntegerField(default=0)
    income_year_end = models.IntegerField(default=0)
    document_name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploaded_documents')
    description = models.CharField(max_length=250, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tax_payer.name} Document'

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(Document, self).delete(*args, **kwargs)


class OtherIncome(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    interest_from_mutual_fund_unit_fund = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cash_dividend_from_company_listed_in_stock_exchange = models.DecimalField(max_digits=20, decimal_places=2,
                                                                              null=True, blank=True)
    interest_income_from_wedb = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    us_dollar_premium_investment_bond = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pound_sterling_premium_investment_bond = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    euro_premium_investment_bond = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    investment_in_pensioners_savings_instrument = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                      blank=True)
    sanchaypatra_income = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    others = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.tax_payer.name} OtherIncome'

    @property
    def get_interest_from_mutual_fund_unit_fund(self):
        if self.interest_from_mutual_fund_unit_fund:
            return self.interest_from_mutual_fund_unit_fund
        else:
            return 0

    @property
    def get_cash_dividend_from_company_listed_in_stock_exchange(self):
        if self.cash_dividend_from_company_listed_in_stock_exchange:
            return self.cash_dividend_from_company_listed_in_stock_exchange
        else:
            return 0

    @property
    def get_interest_income_from_wedb(self):
        if self.interest_income_from_wedb:
            return self.interest_income_from_wedb
        else:
            return 0

    @property
    def get_us_dollar_premium_investment_bond(self):
        if self.us_dollar_premium_investment_bond:
            return self.us_dollar_premium_investment_bond
        else:
            return 0

    @property
    def get_pound_sterling_premium_investment_bond(self):
        if self.pound_sterling_premium_investment_bond:
            return self.pound_sterling_premium_investment_bond
        else:
            return 0

    @property
    def get_euro_premium_investment_bond(self):
        if self.euro_premium_investment_bond:
            return self.euro_premium_investment_bond
        else:
            return 0

    @property
    def get_sanchaypatra_income(self):
        if self.sanchaypatra_income:
            return self.sanchaypatra_income
        else:
            return 0

    @property
    def get_others(self):
        if self.others:
            return self.others
        else:
            return 0

    @property
    def get_total(self):
        return self.get_interest_from_mutual_fund_unit_fund + \
               self.get_cash_dividend_from_company_listed_in_stock_exchange + \
               self.get_interest_income_from_wedb + self.get_us_dollar_premium_investment_bond + \
               self.get_pound_sterling_premium_investment_bond + self.get_euro_premium_investment_bond + \
               self.get_sanchaypatra_income + self.get_others


class TaxRebate(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    life_insurance_premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    life_insurance_premium_policy_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    contribution_to_pf_as_per_act_1925 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    self_and_employers_contribution_to_pf = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    contribution_to_super_annuation_fund = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    investment_in_approved_debenture_or_stock_or_shares = models.DecimalField(max_digits=20, decimal_places=2,
                                                                              null=True, blank=True)
    contribution_to_dps = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    contribution_to_benevolent_fund_and_group_insurance_premium = models.DecimalField(max_digits=20, decimal_places=2,
                                                                                      null=True, blank=True)
    contribution_to_zakat_fund = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    investment_in_savings_certificates_sanchaypatra = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                          blank=True)
    investment_in_bangladesh_govt_treasury_bond = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                      blank=True)
    donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    donation_to_a_charitable_hospital_recognized_by_nbr = models.DecimalField(max_digits=20, decimal_places=2,
                                                                              null=True, blank=True)
    donation_to_organizations_set_up_for_the_welfare_of_retarded_people = models.DecimalField(max_digits=20,
                                                                                              decimal_places=2,
                                                                                              null=True, blank=True)
    contribution_to_national_level_institution_set_up_in_memory_of_liberation_war = models.DecimalField(max_digits=20,
                                                                                                        decimal_places=2,
                                                                                                        null=True,
                                                                                                        blank=True)
    contribution_to_liberation_war_museum = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    contribution_to_aga_khan_development_network = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                       blank=True)
    contribution_to_asiatic_society_bangladesh = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                     blank=True)
    donation_to_icddrb = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    donation_to_crp = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    donation_to_educational_institution_recognized_by_government = models.DecimalField(max_digits=20, decimal_places=2,
                                                                                       null=True, blank=True)
    contribution_to_ahsania_mission_cancer_hospital = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                                                                          blank=True)
    mutual_fund = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.tax_payer.name} TaxRebate'

    @property
    def get_life_insurance_premium(self):
        if self.life_insurance_premium:
            return self.life_insurance_premium
        else:
            return 0

    @property
    def get_life_insurance_premium_policy_value(self):
        if self.life_insurance_premium_policy_value:
            return self.life_insurance_premium_policy_value
        else:
            return 0

    @property
    def get_contribution_to_pf_as_per_act_1925(self):
        if self.contribution_to_pf_as_per_act_1925:
            return self.contribution_to_pf_as_per_act_1925
        else:
            return 0

    @property
    def get_self_and_employers_contribution_to_pf(self):
        if self.self_and_employers_contribution_to_pf:
            return self.self_and_employers_contribution_to_pf
        else:
            return 0

    @property
    def get_contribution_to_super_annuation_fund(self):
        if self.contribution_to_super_annuation_fund:
            return self.contribution_to_super_annuation_fund
        else:
            return 0

    @property
    def get_investment_in_approved_debenture_or_stock_or_shares(self):
        if self.investment_in_approved_debenture_or_stock_or_shares:
            return self.investment_in_approved_debenture_or_stock_or_shares
        else:
            return 0

    @property
    def get_contribution_to_dps(self):
        if self.contribution_to_dps:
            return self.contribution_to_dps
        else:
            return 0

    @property
    def get_contribution_to_benevolent_fund_and_group_insurance_premium(self):
        if self.contribution_to_benevolent_fund_and_group_insurance_premium:
            return self.contribution_to_benevolent_fund_and_group_insurance_premium
        else:
            return 0

    @property
    def get_contribution_to_zakat_fund(self):
        if self.contribution_to_zakat_fund:
            return self.contribution_to_zakat_fund
        else:
            return 0

    @property
    def get_investment_in_savings_certificates_sanchaypatra(self):
        if self.investment_in_savings_certificates_sanchaypatra:
            return self.investment_in_savings_certificates_sanchaypatra
        else:
            return 0

    @property
    def get_investment_in_bangladesh_govt_treasury_bond(self):
        if self.investment_in_bangladesh_govt_treasury_bond:
            return self.investment_in_bangladesh_govt_treasury_bond
        else:
            return 0

    @property
    def get_donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation(self):
        if self.donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation:
            return self.donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation
        else:
            return 0

    @property
    def get_donation_to_a_charitable_hospital_recognized_by_nbr(self):
        if self.donation_to_a_charitable_hospital_recognized_by_nbr:
            return self.donation_to_a_charitable_hospital_recognized_by_nbr
        else:
            return 0

    @property
    def get_donation_to_organizations_set_up_for_the_welfare_of_retarded_people(self):
        if self.donation_to_organizations_set_up_for_the_welfare_of_retarded_people:
            return self.donation_to_organizations_set_up_for_the_welfare_of_retarded_people
        else:
            return 0

    @property
    def get_contribution_to_national_level_institution_set_up_in_memory_of_liberation_war(self):
        if self.contribution_to_national_level_institution_set_up_in_memory_of_liberation_war:
            return self.contribution_to_national_level_institution_set_up_in_memory_of_liberation_war
        else:
            return 0

    @property
    def get_contribution_to_liberation_war_museum(self):
        if self.contribution_to_liberation_war_museum:
            return self.contribution_to_liberation_war_museum
        else:
            return 0

    @property
    def get_contribution_to_aga_khan_development_network(self):
        if self.contribution_to_aga_khan_development_network:
            return self.contribution_to_aga_khan_development_network
        else:
            return 0

    @property
    def get_contribution_to_asiatic_society_bangladesh(self):
        if self.contribution_to_asiatic_society_bangladesh:
            return self.contribution_to_asiatic_society_bangladesh
        else:
            return 0

    @property
    def get_donation_to_icddrb(self):
        if self.donation_to_icddrb:
            return self.donation_to_icddrb
        else:
            return 0

    @property
    def get_donation_to_crp(self):
        if self.donation_to_crp:
            return self.donation_to_crp
        else:
            return 0

    @property
    def get_donation_to_educational_institution_recognized_by_government(self):
        if self.donation_to_educational_institution_recognized_by_government:
            return self.donation_to_educational_institution_recognized_by_government
        else:
            return 0

    @property
    def get_contribution_to_ahsania_mission_cancer_hospital(self):
        if self.contribution_to_ahsania_mission_cancer_hospital:
            return self.contribution_to_ahsania_mission_cancer_hospital
        else:
            return 0

    @property
    def get_mutual_fund(self):
        if self.mutual_fund:
            return self.mutual_fund
        else:
            return 0

    @property
    def get_total(self):
        return self.get_life_insurance_premium + self.get_contribution_to_pf_as_per_act_1925 + \
               self.get_self_and_employers_contribution_to_pf + self.get_contribution_to_super_annuation_fund + \
               self.get_investment_in_approved_debenture_or_stock_or_shares + self.get_contribution_to_dps + \
               self.get_contribution_to_benevolent_fund_and_group_insurance_premium + \
               self.get_contribution_to_zakat_fund + self.get_investment_in_savings_certificates_sanchaypatra + \
               self.get_investment_in_bangladesh_govt_treasury_bond + \
               self.get_donation_to_national_level_institution_set_up_in_the_memory_of_father_of_the_nation + \
               self.get_donation_to_a_charitable_hospital_recognized_by_nbr + \
               self.get_donation_to_organizations_set_up_for_the_welfare_of_retarded_people + \
               self.get_contribution_to_national_level_institution_set_up_in_memory_of_liberation_war + \
               self.get_contribution_to_liberation_war_museum + \
               self.get_contribution_to_aga_khan_development_network + \
               self.get_contribution_to_asiatic_society_bangladesh + self.get_donation_to_icddrb + \
               self.get_donation_to_crp + self.get_donation_to_educational_institution_recognized_by_government + \
               self.get_contribution_to_ahsania_mission_cancer_hospital + self.get_mutual_fund


class DeductionAtSource(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    deduction_description = models.CharField(max_length=100, null=True, blank=True)
    tax_deducted_at_source = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} DeductionAtSource'

    @property
    def get_deduction_description(self):
        if self.deduction_description:
            return self.deduction_description
        else:
            return ""

    @property
    def get_tax_deducted_at_source(self):
        if self.tax_deducted_at_source:
            return self.tax_deducted_at_source
        else:
            return 0


ADVANCE_TAX_PAID_TYPE = [
    ('CarAdvanceTax', 'Car Advance Tax'),
    ('Other', 'Other')
]


class AdvanceTax(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=ADVANCE_TAX_PAID_TYPE, default='Other')
    advance_description = models.CharField(max_length=100, null=True, blank=True)
    advance_paid_tax = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} AdvanceTax'

    @property
    def get_type(self):
        if self.type:
            if self.type == 'CarAdvanceTax':
                return 'Car Advance Tax'
            return self.type
        else:
            return ""

    @property
    def get_advance_description(self):
        if self.advance_description:
            return self.advance_description
        else:
            return ""

    @property
    def get_advance_paid_tax(self):
        if self.advance_paid_tax:
            return self.advance_paid_tax
        else:
            return 0


class TaxRefund(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    refund = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} TaxRefund'

    @property
    def get_refund(self):
        if self.refund:
            return self.refund
        else:
            return 0


class Assets(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    income_year_beg = models.IntegerField(default=0)
    income_year_end = models.IntegerField(default=0)
    business_capital = models.BooleanField(null=True)
    directors_shareholding_assets = models.BooleanField(null=True)
    non_agricultural_property = models.BooleanField(null=True)
    agricultural_property = models.BooleanField(null=True)
    investments = models.BooleanField(null=True)
    motor_vehicle = models.BooleanField(null=True)
    furniture = models.BooleanField(null=True)
    jewellery = models.BooleanField(null=True)
    electronic_equipment = models.BooleanField(null=True)
    cash_assets = models.BooleanField(null=True)
    other_assets = models.BooleanField(null=True)
    other_assets_receipt = models.BooleanField(null=True)
    previous_year_net_wealth = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Assets'

    @property
    def has_business_capital(self):
        if self.business_capital is not None:
            if self.business_capital:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_business_capital(self):
        if self.business_capital is not None:
            if self.business_capital:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_directors_shareholding_assets(self):
        if self.directors_shareholding_assets is not None:
            if self.directors_shareholding_assets:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_directors_shareholding_assets(self):
        if self.directors_shareholding_assets is not None:
            if self.directors_shareholding_assets:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_non_agricultural_property(self):
        if self.non_agricultural_property is not None:
            if self.non_agricultural_property:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_non_agricultural_property(self):
        if self.non_agricultural_property is not None:
            if self.non_agricultural_property:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_agricultural_property(self):
        if self.agricultural_property is not None:
            if self.agricultural_property:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_agricultural_property(self):
        if self.agricultural_property is not None:
            if self.agricultural_property:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_investments(self):
        if self.investments is not None:
            if self.investments:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_investments(self):
        if self.investments is not None:
            if self.investments:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_motor_vehicle(self):
        if self.motor_vehicle is not None:
            if self.motor_vehicle:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_motor_vehicle(self):
        if self.motor_vehicle is not None:
            if self.motor_vehicle:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_furniture(self):
        if self.furniture is not None:
            if self.furniture:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_furniture(self):
        if self.furniture is not None:
            if self.furniture:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_jewellery(self):
        if self.jewellery is not None:
            if self.jewellery:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_jewellery(self):
        if self.jewellery is not None:
            if self.jewellery:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_electronic_equipment(self):
        if self.electronic_equipment is not None:
            if self.electronic_equipment:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_electronic_equipment(self):
        if self.electronic_equipment is not None:
            if self.electronic_equipment:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_cash_assets(self):
        if self.cash_assets is not None:
            if self.cash_assets:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_cash_assets(self):
        if self.cash_assets is not None:
            if self.cash_assets:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_other_assets(self):
        if self.other_assets is not None:
            if self.other_assets:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_other_assets(self):
        if self.other_assets is not None:
            if self.other_assets:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_other_assets_receipt(self):
        if self.other_assets_receipt is not None:
            if self.other_assets_receipt:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_other_assets_receipt(self):
        if self.other_assets_receipt is not None:
            if self.other_assets_receipt:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_previous_year_net_wealth(self):
        if self.previous_year_net_wealth is not None:
            if self.previous_year_net_wealth:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_previous_year_net_wealth(self):
        if self.previous_year_net_wealth is not None:
            if self.previous_year_net_wealth:
                return ""
            else:
                return "checked"
        else:
            return ""


class AgriculturalProperty(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    property_description = models.CharField(max_length=100, null=True, blank=True)
    property_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} AgriculturalProperty'

    @property
    def get_property_description(self):
        if self.property_description:
            return self.property_description
        else:
            return ""

    @property
    def get_property_value(self):
        if self.property_value:
            return self.property_value
        else:
            return 0


INVESTMENT_TYPE = [
    ('Shares/Debentures', 'Shares/Debentures'),
    ('Saving Certificate/Unit Certificate/Bond', 'Saving Certificate/Unit Certificate/Bond'),
    ('Prize Bond/Saving Scheme/FDR/DPS', 'Prize Bond/Saving Scheme/FDR/DPS'),
    ('Loans Given', 'Loans Given'),
    ('Other Investment', 'Other Investment')
]


class Investment(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    type = models.CharField(max_length=100, choices=INVESTMENT_TYPE, default='Shares/Debentures')
    description = models.CharField(max_length=250, null=True, blank=True)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Investment'

    @property
    def get_type(self):
        if self.type:
            return self.type
        else:
            return ""

    @property
    def get_description(self):
        if self.description:
            return self.description
        else:
            return ""

    @property
    def get_value(self):
        if self.value:
            return self.value
        else:
            return 0


class MotorVehicle(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    brand_or_type = models.CharField(max_length=100, null=True)
    reg_no = models.CharField(max_length=50, null=True)
    engine_capacity = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} MotorVehicle'

    @property
    def get_brand_or_type(self):
        if self.brand_or_type:
            return self.brand_or_type
        else:
            return ""

    @property
    def get_reg_no(self):
        if self.reg_no:
            return self.reg_no
        else:
            return ""

    @property
    def get_engine_capacity(self):
        if self.engine_capacity:
            return self.engine_capacity
        else:
            return ""

    @property
    def get_value(self):
        if self.value:
            return self.value
        else:
            return 0


class Furniture(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    furniture_description = models.CharField(max_length=100, null=True, blank=True)
    furniture_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Furniture'

    @property
    def get_furniture_description(self):
        if self.furniture_description:
            return self.furniture_description
        else:
            return ""

    @property
    def get_furniture_value(self):
        if self.furniture_value:
            return self.furniture_value
        else:
            return 0


class Jewellery(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    jewellery_description = models.CharField(max_length=100, null=True, blank=True)
    jewellery_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Jewellery'

    @property
    def get_jewellery_description(self):
        if self.jewellery_description:
            return self.jewellery_description
        else:
            return ""

    @property
    def get_jewellery_value(self):
        if self.jewellery_value:
            return self.jewellery_value
        else:
            return 0


class ElectronicEquipment(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    equipment_description = models.CharField(max_length=100, null=True, blank=True)
    equipment_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} ElectronicEquipment'

    @property
    def get_equipment_description(self):
        if self.equipment_description:
            return self.equipment_description
        else:
            return ""

    @property
    def get_equipment_value(self):
        if self.equipment_value:
            return self.equipment_value
        else:
            return 0


class CashAssets(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    cash_in_hand = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    cash_at_bank = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_fund = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_deposits = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.tax_payer.name} CashAssets'

    @property
    def get_cash_in_hand(self):
        if self.cash_in_hand:
            return self.cash_in_hand
        else:
            return 0

    @property
    def get_cash_at_bank(self):
        if self.cash_at_bank:
            return self.cash_at_bank
        else:
            return 0

    @property
    def get_other_fund(self):
        if self.other_fund:
            return self.other_fund
        else:
            return 0

    @property
    def get_other_deposits(self):
        if self.other_deposits:
            return self.other_deposits
        else:
            return 0


class OtherAssets(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    asset_description = models.CharField(max_length=100, null=True, blank=True)
    asset_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} OtherAssets'

    @property
    def get_asset_description(self):
        if self.asset_description:
            return self.asset_description
        else:
            return ""

    @property
    def get_asset_value(self):
        if self.asset_value:
            return self.asset_value
        else:
            return 0


class OtherAssetsReceipt(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    other_asset_description = models.CharField(max_length=100, null=True, blank=True)
    other_asset_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} OtherAssetsReceipt'

    @property
    def get_other_asset_description(self):
        if self.other_asset_description:
            return self.other_asset_description
        else:
            return ""

    @property
    def get_other_asset_value(self):
        if self.other_asset_value:
            return self.other_asset_value
        else:
            return 0


class PreviousYearNetWealth(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    wealth_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} PreviousYearNetWealth'

    @property
    def get_wealth_value(self):
        if self.wealth_value:
            return self.wealth_value
        else:
            return 0


class Liabilities(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    income_year_beg = models.IntegerField(default=0)
    income_year_end = models.IntegerField(default=0)
    mortgages = models.BooleanField(null=True)
    unsecured_loans = models.BooleanField(null=True)
    bank_loans = models.BooleanField(null=True)
    other_liabilities = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Liabilities'

    @property
    def has_mortgages(self):
        if self.mortgages is not None:
            if self.mortgages:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_mortgages(self):
        if self.mortgages is not None:
            if self.mortgages:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_unsecured_loans(self):
        if self.unsecured_loans is not None:
            if self.unsecured_loans:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_unsecured_loans(self):
        if self.unsecured_loans is not None:
            if self.unsecured_loans:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_bank_loans(self):
        if self.bank_loans is not None:
            if self.bank_loans:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_bank_loans(self):
        if self.bank_loans is not None:
            if self.bank_loans:
                return ""
            else:
                return "checked"
        else:
            return ""

    @property
    def has_other_liabilities(self):
        if self.other_liabilities is not None:
            if self.other_liabilities:
                return "checked"
            else:
                return ""
        else:
            return ""

    @property
    def has_no_other_liabilities(self):
        if self.other_liabilities is not None:
            if self.other_liabilities:
                return ""
            else:
                return "checked"
        else:
            return ""


class Mortgage(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    mortgage_description = models.CharField(max_length=100, null=True, blank=True)
    mortgage_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} Mortgage'

    @property
    def get_mortgage_description(self):
        if self.mortgage_description:
            return self.mortgage_description
        else:
            return ""

    @property
    def get_mortgage_value(self):
        if self.mortgage_value:
            return self.mortgage_value
        else:
            return 0


class UnsecuredLoan(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    unsecured_loan_description = models.CharField(max_length=100, null=True, blank=True)
    unsecured_loan_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} UnsecuredLoan'

    @property
    def get_unsecured_loan_description(self):
        if self.unsecured_loan_description:
            return self.unsecured_loan_description
        else:
            return ""

    @property
    def get_unsecured_loan_value(self):
        if self.unsecured_loan_value:
            return self.unsecured_loan_value
        else:
            return 0


class BankLoan(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    bank_loan_description = models.CharField(max_length=100, null=True, blank=True)
    bank_loan_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} BankLoan'

    @property
    def get_bank_loan_description(self):
        if self.bank_loan_description:
            return self.bank_loan_description
        else:
            return ""

    @property
    def get_bank_loan_value(self):
        if self.bank_loan_value:
            return self.bank_loan_value
        else:
            return 0


class OtherLiability(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    other_liability_description = models.CharField(max_length=100, null=True, blank=True)
    other_liability_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.tax_payer.name} OtherLiability'

    @property
    def get_other_liability_description(self):
        if self.other_liability_description:
            return self.other_liability_description
        else:
            return ""

    @property
    def get_other_liability_value(self):
        if self.other_liability_value:
            return self.other_liability_value
        else:
            return 0


class Expense(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    financial_year_beg = models.IntegerField(default=0)
    financial_year_end = models.IntegerField(default=0)
    food_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    food_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    accommodation_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    accommodation_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    transportation_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    transportation_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    other_transportation_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_transportation_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    electricity_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    electricity_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    gas_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    gas_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    water_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    water_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    telephone_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    telephone_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    other_household_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_household_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    children_education_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    children_education_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    travel_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    travel_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    festival_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    festival_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    donation_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    donation_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    other_special_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_special_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    other_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    other_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    tax_at_source_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    tax_at_source_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    last_year_paid_tax_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    last_year_paid_tax_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    loss_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    loss_expense_comment = models.CharField(max_length=20, null=True, blank=True)
    gift_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    gift_expense_comment = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.tax_payer.name} Expense'

    @property
    def get_food_expense(self):
        if self.food_expense:
            return self.food_expense
        else:
            return 0

    @property
    def get_food_expense_comment(self):
        if self.food_expense_comment:
            return self.food_expense_comment
        else:
            return ""

    @property
    def get_accommodation_expense(self):
        if self.accommodation_expense:
            return self.accommodation_expense
        else:
            return 0

    @property
    def get_accommodation_expense_comment(self):
        if self.accommodation_expense_comment:
            return self.accommodation_expense_comment
        else:
            return ""

    @property
    def get_transportation_expense(self):
        if self.transportation_expense:
            return self.transportation_expense
        else:
            return 0

    @property
    def get_transportation_expense_comment(self):
        if self.transportation_expense_comment:
            return self.transportation_expense_comment
        else:
            return ""

    @property
    def get_other_transportation_expense(self):
        if self.other_transportation_expense:
            return self.other_transportation_expense
        else:
            return 0

    @property
    def get_other_transportation_expense_comment(self):
        if self.other_transportation_expense_comment:
            return self.other_transportation_expense_comment
        else:
            return ""

    @property
    def get_electricity_expense(self):
        if self.electricity_expense:
            return self.electricity_expense
        else:
            return 0

    @property
    def get_electricity_expense_comment(self):
        if self.electricity_expense_comment:
            return self.electricity_expense_comment
        else:
            return ""

    @property
    def get_gas_expense(self):
        if self.gas_expense:
            return self.gas_expense
        else:
            return 0

    @property
    def get_gas_expense_comment(self):
        if self.gas_expense_comment:
            return self.gas_expense_comment
        else:
            return ""

    @property
    def get_water_expense(self):
        if self.water_expense:
            return self.water_expense
        else:
            return 0

    @property
    def get_water_expense_comment(self):
        if self.water_expense_comment:
            return self.water_expense_comment
        else:
            return ""

    @property
    def get_telephone_expense(self):
        if self.telephone_expense:
            return self.telephone_expense
        else:
            return 0

    @property
    def get_telephone_expense_comment(self):
        if self.telephone_expense_comment:
            return self.telephone_expense_comment
        else:
            return ""

    @property
    def get_other_household_expense(self):
        if self.other_household_expense:
            return self.other_household_expense
        else:
            return 0

    @property
    def get_other_household_expense_comment(self):
        if self.other_household_expense_comment:
            return self.other_household_expense_comment
        else:
            return ""

    @property
    def get_children_education_expense(self):
        if self.children_education_expense:
            return self.children_education_expense
        else:
            return 0

    @property
    def get_children_education_expense_comment(self):
        if self.children_education_expense_comment:
            return self.children_education_expense_comment
        else:
            return ""

    @property
    def get_travel_expense(self):
        if self.travel_expense:
            return self.travel_expense
        else:
            return 0

    @property
    def get_travel_expense_comment(self):
        if self.travel_expense_comment:
            return self.travel_expense_comment
        else:
            return ""

    @property
    def get_festival_expense(self):
        if self.festival_expense:
            return self.festival_expense
        else:
            return 0

    @property
    def get_festival_expense_comment(self):
        if self.festival_expense_comment:
            return self.festival_expense_comment
        else:
            return ""

    @property
    def get_donation_expense(self):
        if self.donation_expense:
            return self.donation_expense
        else:
            return 0

    @property
    def get_donation_expense_comment(self):
        if self.donation_expense_comment:
            return self.donation_expense_comment
        else:
            return ""

    @property
    def get_other_special_expense(self):
        if self.other_special_expense:
            return self.other_special_expense
        else:
            return 0

    @property
    def get_other_special_expense_comment(self):
        if self.other_special_expense_comment:
            return self.other_special_expense_comment
        else:
            return ""

    @property
    def get_other_expense(self):
        if self.other_expense:
            return self.other_expense
        else:
            return 0

    @property
    def get_other_expense_comment(self):
        if self.other_expense_comment:
            return self.other_expense_comment
        else:
            return ""

    @property
    def get_tax_at_source_expense(self):
        if self.tax_at_source_expense:
            return self.tax_at_source_expense
        else:
            return 0

    @property
    def get_tax_at_source_expense_comment(self):
        if self.tax_at_source_expense_comment:
            return self.tax_at_source_expense_comment
        else:
            return ""

    @property
    def get_last_year_paid_tax_expense(self):
        if self.last_year_paid_tax_expense:
            return self.last_year_paid_tax_expense
        else:
            return 0

    @property
    def get_last_year_paid_tax_expense_comment(self):
        if self.last_year_paid_tax_expense_comment:
            return self.last_year_paid_tax_expense_comment
        else:
            return ""

    @property
    def get_loss_expense(self):
        if self.loss_expense:
            return self.loss_expense
        else:
            return 0

    @property
    def get_loss_expense_comment(self):
        if self.loss_expense_comment:
            return self.loss_expense_comment
        else:
            return ""

    @property
    def get_gift_expense(self):
        if self.gift_expense:
            return self.gift_expense
        else:
            return 0

    @property
    def get_gift_expense_comment(self):
        if self.gift_expense_comment:
            return self.gift_expense_comment
        else:
            return ""

    @property
    def get_total(self):
        total = 0

        for attr, value in self.__dict__.items():
            if isinstance(value, Decimal):
                total += value

        return total
        