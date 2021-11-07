import re
from decimal import Decimal

from taxlover.constants import INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT, INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT, \
    INDIVIDUAL_TAX_PAYER_THIRD_SLAB_LIMIT, INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_LIMIT, \
    INDIVIDUAL_TAX_PAYER_FIFTH_SLAB_LIMIT, INDIVIDUAL_TAX_PAYER_FIRST_SLAB_TAX_RATE, \
    INDIVIDUAL_TAX_PAYER_SECOND_SLAB_TAX_RATE, INDIVIDUAL_TAX_PAYER_THIRD_SLAB_TAX_RATE, \
    INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_TAX_RATE, INDIVIDUAL_TAX_PAYER_FIFTH_SLAB_TAX_RATE, \
    INDIVIDUAL_TAX_PAYER_SIXTH_SLAB_TAX_RATE, INDIVIDUAL_TAX_PAYER_TAX_REBATE_RATE_01, \
    INDIVIDUAL_TAX_PAYER_TAX_REBATE_TAXABLE_AMOUNT_SLAB, INDIVIDUAL_TAX_PAYER_TAX_REBATE_RATE_02, \
    INDIVIDUAL_TAX_PAYER_INVESTMENT_RATE_ON_TAXABLE_AMOUNT, INDIVIDUAL_TAX_PAYER_INVESTMENT_MAX_LIMIT
from taxlover.models import TaxPayer, Income, Salary, OtherIncome, Assets, Liabilities
import datetime

from taxlover.services.html_parser import strip_tags


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
    else:
        return value


def add_comma_whole(value):
    if value:
        return f'{value:,.0f}'
    else:
        return value


def has_other_income(user_id):
    financial_year_beg, financial_year_end = get_income_years()

    return OtherIncome.objects.filter(tax_payer_id=user_id,
                                      financial_year_beg=financial_year_beg,
                                      financial_year_end=financial_year_end).exists()


def set_form_validation_errors(error_dictionary, fields_dictionary):
    for key in error_dictionary:
        error_text = strip_tags(str(error_dictionary[key]))
        fields_dictionary[key].widget.attrs.update({'class': 'form-control is-invalid', 'title': error_text})


def set_form_initial_value(initial_dictionary):
    for key in initial_dictionary:
        if initial_dictionary[key] and not isinstance(initial_dictionary[key], str):
            initial_dictionary[key] = add_comma(initial_dictionary[key])


def copy_request(request):
    request_copy = request.POST.copy()

    for key in request_copy:
        if key != 'csrfmiddlewaretoken':
            val = remove_comma(request_copy[key])
            request_copy[key] = val

    return request_copy


def create_or_get_current_assets_obj(user_id):
    income_year_beg, income_year_end = get_income_years()

    try:
        latest_assets = Assets.objects.get(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                           income_year_end=income_year_end)
    except Assets.DoesNotExist:
        latest_assets = Assets.objects.create(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                              income_year_end=income_year_end)
    return latest_assets


def create_or_get_current_liabilities_obj(user_id):
    income_year_beg, income_year_end = get_income_years()

    try:
        latest_liabilities = Liabilities.objects.get(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                                     income_year_end=income_year_end)
    except Liabilities.DoesNotExist:
        latest_liabilities = Liabilities.objects.create(tax_payer_id=user_id, income_year_beg=income_year_beg,
                                                        income_year_end=income_year_end)
    return latest_liabilities


def get_gross_tax_before_tax_rebate(total_taxable):
    first_slab_amount = INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT
    second_slab_amount = max(min(
        total_taxable - INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT, INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT), 0)
    third_slab_amount = max(min(
        total_taxable - INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT,
        INDIVIDUAL_TAX_PAYER_THIRD_SLAB_LIMIT), 0)
    fourth_slab_amount = max(min(
        total_taxable - INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT -
        INDIVIDUAL_TAX_PAYER_THIRD_SLAB_LIMIT, INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_LIMIT), 0)
    fifth_slab_amount = max(min(
        total_taxable - INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT -
        INDIVIDUAL_TAX_PAYER_THIRD_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_LIMIT,
        INDIVIDUAL_TAX_PAYER_FIFTH_SLAB_LIMIT), 0)
    sixth_slab_amount = max(
        total_taxable - INDIVIDUAL_TAX_PAYER_FIRST_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_SECOND_SLAB_LIMIT -
        INDIVIDUAL_TAX_PAYER_THIRD_SLAB_LIMIT - INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_LIMIT -
        INDIVIDUAL_TAX_PAYER_FIFTH_SLAB_LIMIT, 0)

    gross_tax_before_tax_rebate = first_slab_amount * INDIVIDUAL_TAX_PAYER_FIRST_SLAB_TAX_RATE + \
                                  second_slab_amount * INDIVIDUAL_TAX_PAYER_SECOND_SLAB_TAX_RATE + \
                                  third_slab_amount * INDIVIDUAL_TAX_PAYER_THIRD_SLAB_TAX_RATE + \
                                  fourth_slab_amount * INDIVIDUAL_TAX_PAYER_FOURTH_SLAB_TAX_RATE + \
                                  fifth_slab_amount * INDIVIDUAL_TAX_PAYER_FIFTH_SLAB_TAX_RATE + \
                                  sixth_slab_amount * INDIVIDUAL_TAX_PAYER_SIXTH_SLAB_TAX_RATE

    return gross_tax_before_tax_rebate


def get_tax_rebate(total_taxable, max_investment_amount):
    tax_rebate = (max_investment_amount * INDIVIDUAL_TAX_PAYER_TAX_REBATE_RATE_01) \
        if (total_taxable < INDIVIDUAL_TAX_PAYER_TAX_REBATE_TAXABLE_AMOUNT_SLAB) \
        else (max_investment_amount * INDIVIDUAL_TAX_PAYER_TAX_REBATE_RATE_02)

    return tax_rebate


def get_net_tax_after_rebate(gross_tax_before_tax_rebate, tax_rebate):
    return min(gross_tax_before_tax_rebate - tax_rebate, gross_tax_before_tax_rebate)


def get_max_investment_amount(total_invested_amount, total_taxable_amount):
    return min(total_taxable_amount * INDIVIDUAL_TAX_PAYER_INVESTMENT_RATE_ON_TAXABLE_AMOUNT, total_invested_amount,
               INDIVIDUAL_TAX_PAYER_INVESTMENT_MAX_LIMIT)
