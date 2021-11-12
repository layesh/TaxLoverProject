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

            self.total_payment_of_tax_charges = self.expense.get_tax_at_source_expense + self.expense.get_last_year_paid_tax_expense

            self.total_lifestyle_expense = self.annual_living_expenditure_and_tax_payments - self.total_payment_of_tax_charges

            self.loss_expense = self.expense.get_loss_expense
            self.gift_expense = self.expense.get_gift_expense

            self.total_transport_expense = self.expense.get_transportation_expense + self.expense.get_other_transportation_expense
            self.total_gas_and_water_expense = self.expense.get_gas_expense + self.expense.get_water_expense
            self.total_gas_or_water_expense_comment = self.expense.get_gas_expense_comment if \
                self.expense.get_gas_expense_comment != '' else self.expense.get_water_expense_comment
            self.total_household_and_utility_expense = self.expense.get_electricity_expense + self.total_gas_and_water_expense + \
                                                       self.expense.get_telephone_expense + self.expense.other_household_expense
            self.total_special_expense = self.expense.get_travel_expense + self.expense.get_festival_expense + \
                                         self.expense.get_donation_expense + self.expense.get_other_special_expense
