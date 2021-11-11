from taxlover.services.expense_service import get_current_financial_year_expense_by_payer
from taxlover.utils import get_income_years


class ExpenseDTO:

    def __init__(self, tax_payer_id):
        self.expense = get_current_financial_year_expense_by_payer(tax_payer_id)

        self.income_year_beg, self.income_year_end = get_income_years()

        if self.expense:
            self.total_expenses = self.expense.get_total
            self.annual_living_expenditure_and_tax_payments = self.total_expenses - self.expense.get_loss_expense - \
                                                              self.expense.get_gift_expense
            self.loss_expense = self.expense.get_loss_expense
            self.gift_expense = self.expense.get_gift_expense
