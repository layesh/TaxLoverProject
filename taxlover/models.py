from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Division(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TaxPayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, null=True)
    e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    dob = models.DateField
    married = models.BooleanField
    spouse_name = models.CharField(max_length=250, null=True)
    spouse_e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    has_differently_abled_children = models.BooleanField
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    resident = models.BooleanField
    nid = models.CharField(max_length=17, null=True)
    differently_abled = models.BooleanField
    fathers_name = models.CharField(max_length=250, null=True)
    mothers_name = models.CharField(max_length=250, null=True)
    num_of_dependent_adult = models.IntegerField
    num_of_dependent_child = models.IntegerField
    gazetted_war_wounded_freedom_fighter = models.BooleanField
    government_employee = models.BooleanField
    RESIDENCE_AREA = (
        (1, 'Dhaka and Chittagong City Corporation'),
        (2, 'Other City Corporation'),
        (3, 'Other Areas')
    )
    residence_area = models.IntegerField(choices=RESIDENCE_AREA, null=True)
    tax_zone = models.IntegerField
    tax_circle = models.IntegerField
    employer_name = models.CharField(max_length=250, null=True)
    employer_address = models.CharField(max_length=250, null=True)
    employer_bin = models.CharField(max_length=20, null=True)
    present_address_line_one = models.CharField(max_length=250, null=True)
    present_address_line_two = models.CharField(max_length=250, null=True)
    present_address_postcode = models.IntegerField
    present_address_division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    present_address_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    same_address = models.BooleanField
    permanent_address = models.CharField(max_length=250, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


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
