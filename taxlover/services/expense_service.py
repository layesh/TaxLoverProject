from taxlover.models import Expense
from taxlover.utils import get_income_years


def get_current_financial_year_expense_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Expense.objects.filter(tax_payer_id=payer_id,
                                  financial_year_beg=financial_year_beg,
                                  financial_year_end=financial_year_end).first()