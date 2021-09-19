from taxlover.services.salary_service import get_total_taxable
from taxlover.utils import get_income_years


class IncomeDTO:

    def __init__(self, salary):
        self.income_year_beg, self.income_year_end = get_income_years()

        self.taxable = get_total_taxable(salary.basic, salary.house_rent, salary.medical)