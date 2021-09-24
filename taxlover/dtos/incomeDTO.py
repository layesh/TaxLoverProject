from taxlover.services.salary_service import get_total_taxable
from taxlover.utils import get_income_years


class IncomeDTO:

    def __init__(self, income, salary):
        self.has_salary_income = income.has_salary_income
        self.has_no_salary_income = income.has_no_salary_income
        if salary:
            self.income_year_beg, self.income_year_end = get_income_years()
            self.salaryId = salary.id
            self.taxable = get_total_taxable(salary)
            self.total = salary.get_total
            self.basic = salary.get_basic
