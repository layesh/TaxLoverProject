from decimal import Decimal
from ExtractTable import ExtractTable
from django.db.models import Sum

from taxlover.constants import EXTRACT_TABLE_API_KEY, HOUSE_RENT_MONTHLY_EXEMPTED_RATE, MEDICAL_YEARLY_EXEMPTED_RATE, \
    CONVEYANCE_YEARLY_EXEMPTED_RATE
from taxlover.models import Salary, DeductionAtSource, AdvanceTax
from taxlover.utils import parse_data, get_income_years


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

    # TODO: check if table has data
    table_column_length = len(salary_table_data[0].columns)

    salary = Salary()
    salary.tax_payer_id = payer_id
    salary.financial_year_beg, salary.financial_year_end = get_income_years()

    for row_index, row in salary_table_data[0].iterrows():
        # For Nilavo Tech 2021
        # salary_category = str(row[0]).lower()
        # For Nilavo Tech 2022
        salary_category = str(row[1]).lower()

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
        elif 'other allowances' in salary_category:
            salary.other_allowances = parse_data(row, table_column_length)
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

    # For Nilavo Tech 2022
    table_column_length = len(salary_table_data[1].columns)

    for row_index, row in salary_table_data[1].iterrows():
        salary_category = str(row[0]).lower()

        if 'company contribution' in salary_category:
            salary.employers_contribution_to_pf = parse_data(row, table_column_length)
        elif 'own contribution' in salary_category:
            salary.employees_contribution_to_pf = parse_data(row, table_column_length)

    if salary.total_bonus == 0:
        salary.total_bonus = salary.festival_bonus + salary.other_bonus

    total_annual_payment = salary.get_basic + salary.get_house_rent + salary.get_medical + salary.get_conveyance + \
        salary.get_lfa + salary.other_allowances + salary.get_total_bonus + salary.get_employers_contribution_to_pf

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
           salary.get_other_allowances + \
           salary.get_total_bonus + \
           salary.get_employers_contribution_to_pf


def get_current_financial_year_total_tax_deducted_at_source_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    total_deduction_at_source = DeductionAtSource.objects.filter(tax_payer_id=payer_id,
                                                                 financial_year_beg=financial_year_beg,
                                                                 financial_year_end=financial_year_end).aggregate(
        Sum('tax_deducted_at_source'))

    return total_deduction_at_source['tax_deducted_at_source__sum'] if total_deduction_at_source[
                                                                           'tax_deducted_at_source__sum'] is not None \
        else 0


def get_current_financial_year_total_advance_tax_paid_by_payer(payer_id):
    financial_year_beg, financial_year_end = get_income_years()

    total_advance_paid_tax = AdvanceTax.objects.filter(tax_payer_id=payer_id,
                                                       financial_year_beg=financial_year_beg,
                                                       financial_year_end=financial_year_end).aggregate(
        Sum('advance_paid_tax'))

    return total_advance_paid_tax['advance_paid_tax__sum'] if total_advance_paid_tax[
                                                                  'advance_paid_tax__sum'] is not None \
        else 0
