from taxlover.services.salary_service import get_current_financial_year_salary_by_payer


def save_income(latest_income, source, answer, request):
    show_success_message = False

    if source == 'salary':
        if answer == 'yes':
            latest_income.salary = True
        elif answer == 'no':
            show_success_message = True
            latest_income.salary = False
            salary = get_current_financial_year_salary_by_payer(request.user.id)
            if salary:
                salary.delete()
    elif source == 'interest_on_security':
        show_success_message = True
        if answer == 'yes':
            latest_income.interest_on_security = True
        elif answer == 'no':
            latest_income.interest_on_security = False
    elif source == 'rental_property':
        show_success_message = True
        if answer == 'yes':
            latest_income.rental_property = True
        elif answer == 'no':
            latest_income.rental_property = False
    elif source == 'agriculture':
        show_success_message = True
        if answer == 'yes':
            latest_income.agriculture = True
        elif answer == 'no':
            latest_income.agriculture = False
    elif source == 'business':
        show_success_message = True
        if answer == 'yes':
            latest_income.business = True
        elif answer == 'no':
            latest_income.business = False
    elif source == 'share_of_profit_in_firm':
        show_success_message = True
        if answer == 'yes':
            latest_income.share_of_profit_in_firm = True
        elif answer == 'no':
            latest_income.share_of_profit_in_firm = False
    elif source == 'spouse_or_child':
        show_success_message = True
        if answer == 'yes':
            latest_income.spouse_or_child = True
        elif answer == 'no':
            latest_income.spouse_or_child = False
    elif source == 'capital_gains':
        show_success_message = True
        if answer == 'yes':
            latest_income.capital_gains = True
        elif answer == 'no':
            latest_income.capital_gains = False
    elif source == 'other_sources':
        show_success_message = True
        if answer == 'yes':
            latest_income.other_sources = True
        elif answer == 'no':
            latest_income.other_sources = False
    elif source == 'foreign_income':
        show_success_message = True
        if answer == 'yes':
            latest_income.foreign_income = True
        elif answer == 'no':
            latest_income.foreign_income = False
    elif source == 'tax_rebate':
        show_success_message = True
        if answer == 'yes':
            latest_income.tax_rebate = True
        elif answer == 'no':
            latest_income.tax_rebate = False
    elif source == 'tax_deducted_at_source':
        show_success_message = True
        if answer == 'yes':
            latest_income.tax_deducted_at_source = True
        elif answer == 'no':
            latest_income.tax_deducted_at_source = False
    elif source == 'advance_paid_tax':
        show_success_message = True
        if answer == 'yes':
            latest_income.advance_paid_tax = True
        elif answer == 'no':
            latest_income.advance_paid_tax = False
    elif source == 'adjustment_of_tax_refund':
        show_success_message = True
        if answer == 'yes':
            latest_income.adjustment_of_tax_refund = True
        elif answer == 'no':
            latest_income.adjustment_of_tax_refund = False

    latest_income.save()

    return show_success_message
