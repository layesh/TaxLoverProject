from django.contrib import admin

# Register your models here.
from taxlover.models import TaxPayer, Salary, Division, District

admin.site.register(TaxPayer)
admin.site.register(Salary)
admin.site.register(Division)
admin.site.register(District)