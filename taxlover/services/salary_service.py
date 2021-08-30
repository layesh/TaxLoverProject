import pandas as pd
from ExtractTable import ExtractTable

from taxlover.constants import EXTRACT_TABLE_API_KEY
from taxlover.models import Salary
from taxlover.utils import parse_data, get_income_years


def process_and_save_salary(file_name, payer_id):
    extract_table_session = ExtractTable(api_key=EXTRACT_TABLE_API_KEY)
    print(extract_table_session.check_usage())

    file_path = 'media/' + file_name

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

    return total_annual_payment
