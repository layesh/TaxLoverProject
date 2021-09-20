import re
from decimal import Decimal

from taxlover.models import TaxPayer, Income, Salary
import datetime


def parse_data(row, total_columns):
    parsed_data = 0.0

    for i in range(0, total_columns):
        if i == 0:
            regex_matches = re.findall("(\d*\.?\d+|\d{1,3}(,\d{3})*(\.\d+)?)$",
                                       row[i])  # simpler: [0-9]{1,3}(,[0-9]{3})*\.[0-9]+$
            if len(regex_matches) > 0:
                parsed_data = Decimal(remove_comma(regex_matches[0][0]))
                if parsed_data > 0.0:
                    return parsed_data
        else:
            try:
                parsed_data = Decimal(remove_comma(row[i]))
                if parsed_data > 0.0:
                    return parsed_data
            except Exception:
                parsed_data = 0.0

    return parsed_data


def create_or_get_tax_payer_obj(user_id):
    try:
        tax_payer = TaxPayer.objects.get(user_id=user_id)
    except TaxPayer.DoesNotExist:
        tax_payer = TaxPayer.objects.create(user_id=user_id)

    return tax_payer


def create_or_get_current_income_obj(user_id):
    income_year_beg, income_year_end = get_income_years()

    try:
        latest_income = Income.objects.get(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                           income_year_end=income_year_end)
    except Income.DoesNotExist:
        latest_income = Income.objects.create(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                              income_year_end=income_year_end)
    return latest_income


def get_income_years():
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    income_year_beg = current_year - 1 if current_month > 6 else current_year - 2
    income_year_end = income_year_beg + 1

    return income_year_beg, income_year_end


def get_assessment_years():
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    assessment_year_beg = current_year if current_month > 6 else current_year - 1
    assessment_year_end = assessment_year_beg + 1

    return assessment_year_beg, assessment_year_end


def has_salary_data(user_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Salary.objects.filter(tax_payer_id=user_id,
                                 financial_year_beg=financial_year_beg,
                                 financial_year_end=financial_year_end).exists()


def remove_comma(value):
    return value.replace(",", "")


def add_comma(value):
    if value:
        return f'{value:,.2f}'
