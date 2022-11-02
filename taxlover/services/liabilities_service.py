from django.db.models import Sum

from taxlover.models import Mortgage, OtherLiability, BankLoan, UnsecuredLoan, Liabilities
from taxlover.utils import get_income_years, get_previous_income_years


def save_liabilities(latest_liabilities, source, answer, request):
    show_success_message = False

    if source == 'mortgages':
        show_success_message = True
        if answer == 'yes':
            latest_liabilities.mortgages = True
        elif answer == 'no':
            latest_liabilities.mortgages = False
    elif source == 'unsecured_loans':
        show_success_message = True
        if answer == 'yes':
            latest_liabilities.unsecured_loans = True
        elif answer == 'no':
            latest_liabilities.unsecured_loans = False
    elif source == 'bank_loans':
        show_success_message = True
        if answer == 'yes':
            latest_liabilities.bank_loans = True
        elif answer == 'no':
            latest_liabilities.bank_loans = False
    elif source == 'other_liabilities':
        show_success_message = True
        if answer == 'yes':
            latest_liabilities.other_liabilities = True
        elif answer == 'no':
            latest_liabilities.other_liabilities = False

    latest_liabilities.save()

    return show_success_message


def get_mortgages_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return Mortgage.objects.filter(tax_payer_id=payer_id,
                                   financial_year_beg=financial_year_beg,
                                   financial_year_end=financial_year_end)


def get_unsecured_loans_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return UnsecuredLoan.objects.filter(tax_payer_id=payer_id,
                                        financial_year_beg=financial_year_beg,
                                        financial_year_end=financial_year_end)


def get_total_unsecured_loans_value(unsecured_loans):
    total = unsecured_loans.aggregate(Sum('unsecured_loan_value'))

    return total['unsecured_loan_value__sum'] if total['unsecured_loan_value__sum'] is not None else 0


def get_bank_loans_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return BankLoan.objects.filter(tax_payer_id=payer_id,
                                   financial_year_beg=financial_year_beg,
                                   financial_year_end=financial_year_end)


def get_total_mortgage_and_bank_loan_value(mortgages, bank_loans):
    total_mortgage_value = mortgages.aggregate(Sum('mortgage_value'))
    total_bank_loan_value = bank_loans.aggregate(Sum('bank_loan_value'))

    total_value = (total_mortgage_value['mortgage_value__sum'] if total_mortgage_value['mortgage_value__sum'] is not None else 0) + \
                  (total_bank_loan_value['bank_loan_value__sum'] if total_bank_loan_value['bank_loan_value__sum'] is not None else 0)

    return total_value


def get_other_liabilities_by_payer(payer_id, previous_year=None):
    if previous_year:
        financial_year_beg, financial_year_end = get_previous_income_years()
    else:
        financial_year_beg, financial_year_end = get_income_years()

    return OtherLiability.objects.filter(tax_payer_id=payer_id,
                                         financial_year_beg=financial_year_beg,
                                         financial_year_end=financial_year_end)


def get_total_other_liabilities_value(other_liabilities):
    total = other_liabilities.aggregate(Sum('other_liability_value'))

    return total['other_liability_value__sum'] if total['other_liability_value__sum'] is not None else 0


def copy_liabilities_data_from_previous_year(payer_id):
    previous_income_year_beg, previous_income_year_end = get_previous_income_years()

    prev_year_liabilities = Liabilities.objects.get(tax_payer_id=payer_id, income_year_beg=previous_income_year_beg,
                                                    income_year_end=previous_income_year_end)

    income_year_beg, income_year_end = get_income_years()
    prev_year_liabilities.id = None
    prev_year_liabilities.income_year_beg = income_year_beg
    prev_year_liabilities.income_year_end = income_year_end

    prev_year_liabilities.save()

    mortgages = get_mortgages_by_payer(payer_id, True)
    unsecured_loans = get_unsecured_loans_by_payer(payer_id, True)
    bank_loans = get_bank_loans_by_payer(payer_id, True)
    other_liabilities = get_other_liabilities_by_payer(payer_id, True)

    for liabilities in mortgages:
        liabilities.id = None
        liabilities.financial_year_beg = income_year_beg
        liabilities.financial_year_end = income_year_end
        liabilities.save()

    for liabilities in unsecured_loans:
        liabilities.id = None
        liabilities.financial_year_beg = income_year_beg
        liabilities.financial_year_end = income_year_end
        liabilities.save()

    for liabilities in bank_loans:
        liabilities.id = None
        liabilities.financial_year_beg = income_year_beg
        liabilities.financial_year_end = income_year_end
        liabilities.save()

    for liabilities in other_liabilities:
        liabilities.id = None
        liabilities.financial_year_beg = income_year_beg
        liabilities.financial_year_end = income_year_end
        liabilities.save()
