from decimal import Decimal
from enum import Enum

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


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
    # GENDER_CHOICES = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    #     ('T', 'Transgender')
    # )
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
            return self.dob.strftime(("%d/%m/%Y"))
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
    basic = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    house_rent = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    medical = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    conveyance = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    lfa = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    festival_bonus = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    other_bonus = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    employers_contribution_to_pf = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    employees_contribution_to_pf = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    ait = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))

    def __str__(self):
        return f'{self.tax_payer.name} Salary'

    def get_absolute_url(self):
        return reverse('salary-detail', kwargs={'pk': self.pk})


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


class Document(models.Model):
    tax_payer = models.ForeignKey(TaxPayer, on_delete=models.CASCADE)
    income_year_beg = models.IntegerField(default=0)
    income_year_end = models.IntegerField(default=0)
    document_name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploaded_documents')
    description = models.CharField(max_length=250, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
