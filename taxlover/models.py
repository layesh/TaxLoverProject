import os
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
               self.get_total_bonus + self.get_employers_contribution_to_pf


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
    conveyance = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
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
    def get_others(self):
        if self.others:
            return self.others
        else:
            return 0
