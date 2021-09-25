from decimal import Decimal

import pandas as pd
from ExtractTable import ExtractTable

from taxlover.constants import EXTRACT_TABLE_API_KEY, HOUSE_RENT_MONTHLY_EXEMPTED_RATE, MEDICAL_YEARLY_EXEMPTED_RATE, \
    CONVEYANCE_YEARLY_EXEMPTED_RATE
from taxlover.models import Salary
from taxlover.services.html_parser import strip_tags
from taxlover.utils import parse_data, get_income_years, add_comma


def get_current_financial_year_salary_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    return Salary.objects.filter(tax_payer_id=payer_id,
                                 financial_year_beg=financial_year_beg,
                                 financial_year_end=financial_year_end).first()


def process_and_save_salary(salary_statement_document, payer_id):
    extract_table_session = ExtractTable(api_key=EXTRACT_TABLE_API_KEY)
    print(extract_table_session.check_usage())

    file_path = 'media/' + salary_statement_document.file.name

    salary_table_data = extract_table_session.process_file(filepath=file_path,
                                                           output_format="df")

    table_column_length = len(salary_table_data[0].columns)

    salary = Salary()
    salary.tax_payer_id = payer_id
    salary.financial_year_beg, salary.financial_year_end = get_income_years()

    for row_index, row in salary_table_data[0].iterrows():
        salary_category = str(row[0]).lower()
        if 'basic' in salary_category:
            salary.basic = parse_data(row, table_column_length)
        elif 'house rent' in salary_category:
            salary.house_rent = parse_data(row, table_column_length)
        elif 'medical' in salary_category:
            salary.medical = parse_data(row, table_column_length)
        elif 'conveyance' in salary_category:
            salary.conveyance = parse_data(row, table_column_length)
        elif 'leave fare assistance' in salary_category:
            salary.lfa = parse_data(row, table_column_length)
        elif 'festival bonus' in salary_category:
            salary.festival_bonus = parse_data(row, table_column_length)
        elif 'other bonus' in salary_category:
            salary.other_bonus = parse_data(row, table_column_length)
        elif 'total bonus' in salary_category:
            salary.total_bonus = parse_data(row, table_column_length)
        elif 'employer\'s contribution to pf' in salary_category:
            salary.employers_contribution_to_pf = parse_data(row, table_column_length)
        elif 'employee\'s contribution to pf' in salary_category:
            salary.employees_contribution_to_pf = parse_data(row, table_column_length)
        elif 'advance income tax' in salary_category:
            salary.ait = parse_data(row, table_column_length)

    total_annual_payment = salary.get_basic + salary.get_house_rent + salary.get_medical + salary.get_conveyance + \
        salary.get_lfa + salary.get_total_bonus + salary.get_employers_contribution_to_pf

    if total_annual_payment > 0:
        salary.save()
        salary_statement_document.salary = salary

    return total_annual_payment


def get_house_rent_exempted(basic, house_rent):
    return Decimal(min(12 * HOUSE_RENT_MONTHLY_EXEMPTED_RATE, float(basic) * 0.5, Decimal(house_rent)))


def get_medical_exempted(basic, medical):
    return Decimal(min(MEDICAL_YEARLY_EXEMPTED_RATE, float(basic) * 0.1, Decimal(medical)))


def get_conveyance_exempted(conveyance):
    return Decimal(min(CONVEYANCE_YEARLY_EXEMPTED_RATE, Decimal(conveyance)))


def get_total_taxable(salary):
    return salary.get_basic + \
           salary.get_house_rent - get_house_rent_exempted(salary.get_basic, salary.get_house_rent) + \
           salary.get_medical - get_medical_exempted(salary.get_basic, salary.get_medical) + \
           salary.get_conveyance - get_conveyance_exempted(salary.get_conveyance) + \
           salary.get_total_bonus + \
           salary.get_employers_contribution_to_pf


def set_salary_form_initial_value(initial_dictionary):
    for key in initial_dictionary:
        if initial_dictionary[key]:
            initial_dictionary[key] = add_comma(initial_dictionary[key])


def set_salary_form_validation_errors(error_dictionary, fields_dictionary):
    for key in error_dictionary:
        error_text = strip_tags(str(error_dictionary[key]))
        fields_dictionary[key].widget.attrs.update({'class': 'form-control is-invalid', 'title': error_text})
