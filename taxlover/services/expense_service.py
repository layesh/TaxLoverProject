from taxlover.models import Expense
from taxlover.utils import get_income_years, get_previous_income_years


def create_or_get_expense_by_payer(payer_id, do_not_save_object=None):
    financial_year_beg, financial_year_end = get_income_years()

    try:
        latest_expenses = Expense.objects.get(tax_payer_id=payer_id, financial_year_beg=financial_year_beg,
                                              financial_year_end=financial_year_end)
    except Expense.DoesNotExist:
        if do_not_save_object:
            latest_expenses = Expense()
        else:
            latest_expenses = Expense.objects.create(tax_payer_id=payer_id, financial_year_beg=financial_year_beg,
                                                     financial_year_end=financial_year_end)
    return latest_expenses


def copy_expenses_data_from_previous_year(payer_id):
    previous_income_year_beg, previous_income_year_end = get_previous_income_years()

    prev_year_expense = Expense.objects.get(tax_payer_id=payer_id, financial_year_beg=previous_income_year_beg,
                                            financial_year_end=previous_income_year_end)

    income_year_beg, income_year_end = get_income_years()
    prev_year_expense.id = None
    prev_year_expense.financial_year_beg = income_year_beg
    prev_year_expense.financial_year_end = income_year_end

    prev_year_expense.save()

