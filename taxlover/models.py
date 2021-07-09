from decimal import Decimal

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


class TaxPayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, null=True)
    e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    dob = models.DateField(blank=True, null=True)
    married = models.BooleanField(null=True)
    spouse_name = models.CharField(max_length=250, null=True)
    spouse_e_tin = models.CharField(max_length=12, validators=[MinLengthValidator(12)], null=True)
    has_differently_abled_children = models.BooleanField(null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
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

    def __str__(self):
        return self.name

    @property
    def get_e_tin(self):
        if self.e_tin:
            return self.e_tin
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
