from decimal import Decimal

from django.db import models


class TaxPayer(models.Model):
    name = models.CharField(max_length=250)


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
