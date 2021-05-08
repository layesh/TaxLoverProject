from django.contrib import admin

# Register your models here.
from taxlover.models import TaxPayer, Salary

admin.site.register(TaxPayer)
admin.site.register(Salary)
