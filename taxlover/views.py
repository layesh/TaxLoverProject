from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

import json
import pandas as pd
import datetime

from ExtractTable import ExtractTable
from django.contrib.auth.decorators import login_required

from taxlover.constants import EXTRACT_TABLE_API_KEY
from taxlover.dtos.assetsDTO import AssetsDTO
from taxlover.dtos.incomeDTO import IncomeDTO
from taxlover.dtos.taxPayerDTO import TaxPayerDTO
from taxlover.forms import UploadSalaryStatementForm, SalaryForm, OtherIncomeForm, TaxRebateForm, DeductionAtSourceForm, \
    AdvanceTaxPaidForm, TaxRefundForm, AgriculturalPropertyForm, InvestmentForm, MotorVehicleForm, FurnitureForm, \
    JewelleryForm, ElectronicEquipmentForm, OtherAssetsForm, OtherAssetsReceiptForm, PreviousYearNetWealthForm, \
    CashAssetsForm
from taxlover.models import TaxPayer, Salary, Document, OtherIncome, TaxRebate, DeductionAtSource, AdvanceTax, \
    TaxRefund, AgriculturalProperty, Investment, MotorVehicle, Furniture, Jewellery, ElectronicEquipment, CashAssets, \
    PreviousYearNetWealth, OtherAssets, OtherAssetsReceipt
from taxlover.services.assets_service import save_assets, get_current_financial_year_agricultural_property_by_payer, \
    get_current_financial_year_cash_assets_by_payer, \
    get_current_financial_year_previous_year_net_wealth_receipt_by_payer
from taxlover.services.income_service import save_income, get_current_financial_year_other_income_by_payer, \
    get_interest_from_mutual_fund_exempted, get_cash_dividend_exempted, get_current_financial_year_tax_rebate_by_payer, \
    get_life_insurance_premium_allowed, get_contribution_to_dps_allowed, get_current_financial_year_tax_refund_by_payer
from taxlover.services.salary_service import process_and_save_salary, get_house_rent_exempted, \
    get_current_financial_year_salary_by_payer, get_medical_exempted, get_conveyance_exempted
from taxlover.utils import parse_data, create_or_get_tax_payer_obj, create_or_get_current_income_obj, \
    get_assessment_years, get_income_years, has_salary_data, remove_comma, add_comma, has_other_income, \
    set_form_validation_errors, set_form_initial_value, copy_request, create_or_get_current_assets_obj

import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


@login_required
def home(request):
    tax_year_beg, tax_year_end = get_assessment_years()

    context = {
        'salaries': Salary.objects.all(),
        'title': 'Dashboard',
        'tax_year_beg': tax_year_beg,
        'tax_year_end': tax_year_end
    }
    return render(request, 'taxlover/home.html', context)


class SalaryListView(LoginRequiredMixin, ListView):
    model = Salary
    template_name = 'taxlover/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'salaries'
    ordering = ['-id']


class SalaryDetailView(DetailView):
    model = Salary


class SalaryCreateView(LoginRequiredMixin, CreateView):
    model = Salary
    fields = ['financial_year_beg', 'financial_year_end']

    def form_valid(self, form):
        # form.instance.tax_payer = self.request.user
        return super().form_valid(form)


class SalaryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Salary
    fields = ['financial_year_beg', 'financial_year_end']

    def form_valid(self, form):
        # form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        salary = self.get_object()
        if self.request.user.id == salary.tax_payer_id:
            return True
        return False


class SalaryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Salary
    success_url = '/'

    def test_func(self):
        salary = self.get_object()
        if self.request.user.id == salary.tax_payer_id:
            return True
        return False


@login_required
def personal_info(request):
    has_dob_error = False
    has_circle_error = False
    has_zone_error = False

    if request.method == 'POST':
        tax_payer = create_or_get_tax_payer_obj(request.user.id)

        tax_payer.e_tin = request.POST.get('e_tin')
        tax_payer.nid = request.POST.get('nid')
        try:
            tax_payer.dob = datetime.datetime.strptime(request.POST.get('dob'), "%d/%m/%Y").date()
        except ValueError:
            tax_payer.dob = request.POST.get('dob')
            has_dob_error = True
            pass
        tax_payer.mobile_no = request.POST.get('contact_no')

        try:
            tax_payer.tax_circle = int(request.POST.get('tax_circle'))
        except ValueError:
            tax_payer.tax_circle = request.POST.get('tax_circle')
            has_circle_error = True
            pass
        try:
            tax_payer.tax_zone = int(request.POST.get('tax_zone'))
        except ValueError:
            tax_payer.tax_zone = request.POST.get('tax_zone')
            has_zone_error = True
            pass

        tax_payer.name = request.POST.get('full_name')
        tax_payer.fathers_name = request.POST.get('fathers_name')
        tax_payer.mothers_name = request.POST.get('mothers_name')
        tax_payer.present_address_line_one = request.POST.get('present_address_line_one')
        tax_payer.permanent_address = request.POST.get('permanent_address')
        tax_payer.email = request.POST.get('email')
        tax_payer.employer_name = request.POST.get('employer_name')

        tax_payer.resident = request.POST.get('residentRadios') == 'True'
        tax_payer.married = request.POST.get('maritalStatusRadios') == 'True'
        tax_payer.gender = request.POST.get('genderRadios')
        tax_payer.government_employee = request.POST.get('governmentEmployeeRadios') == 'True'

        if tax_payer.is_married:
            tax_payer.spouse_name = request.POST.get('spouse_name')
            tax_payer.spouse_e_tin = request.POST.get('spouse_e_tin')
        else:
            tax_payer.spouse_name = ''
            tax_payer.spouse_e_tin = ''

        tax_payer.gazetted_war_wounded_freedom_fighter = "gazetted_war_wounded_freedom_fighter" in request.POST
        tax_payer.differently_abled = "differently_abled" in request.POST
        tax_payer.aged_65_years_or_more = "aged_65_years_or_more" in request.POST
        tax_payer.has_differently_abled_children = "has_differently_abled_children" in request.POST

        if has_dob_error or has_circle_error or has_zone_error:
            messages.error(request, f'Please correct the errors below, and try again.')
        else:
            tax_payer.save()
            messages.success(request, f'Your personal info has been updated!')
    else:
        tax_payer = create_or_get_tax_payer_obj(request.user.id)

    context = {
        'tax_payer': tax_payer,
        'title': 'Personal Info',
        'has_dob_error': has_dob_error,
        'has_circle_error': has_circle_error,
        'has_zone_error': has_zone_error

    }
    return render(request, 'taxlover/personal-info.html', context)


@login_required
def income(request):
    income_dto = IncomeDTO(request.user.id, False)

    das_form = DeductionAtSourceForm(request.POST)
    atp_form = AdvanceTaxPaidForm(request.POST)
    tr_form = TaxRefundForm(request.POST)

    context = {
        'income_dto': income_dto,
        'title': 'Income',
        'das_form': das_form,
        'atp_form': atp_form,
        'tr_form': tr_form
    }

    return render(request, 'taxlover/income.html', context)


@login_required
def save_income_data(request, source, answer):
    latest_income = create_or_get_current_income_obj(request.user.id)
    show_success_message = save_income(latest_income, source, answer, request)

    if show_success_message:
        messages.success(request, f'Data updated successfully!')

    context = {
        'latest_income': latest_income,
        'title': 'Income'
    }

    if source == 'salary':
        if latest_income.salary:
            if has_salary_data(request.user.id):
                return redirect('salary-info')
            else:
                return render(request, 'taxlover/choose-salary-input.html', context)
        else:
            return redirect('income')
    elif source == 'interest_on_security' or source == 'rental_property' or source == 'agriculture' or \
            source == 'business' or source == 'share_of_profit_in_firm' or source == 'spouse_or_child' or \
            source == 'capital_gains' or source == 'foreign_income' or \
            source == 'tax_deducted_at_source' or source == 'advance_paid_tax' or \
            source == 'adjustment_of_tax_refund':
        return redirect('income')
    elif source == 'other_sources':
        if latest_income.other_sources:
            return redirect('other-income')
        else:
            return redirect('income')
    elif source == 'tax_rebate':
        if latest_income.tax_rebate:
            return redirect('tax_rebate')
        else:
            return redirect('income')


@login_required
def salary_info(request):
    info = request.GET.get('info', '')
    salary = get_current_financial_year_salary_by_payer(request.user.id)
    if not salary:
        financial_year_beg, financial_year_end = get_income_years()
        salary = Salary(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                        financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = SalaryForm(copy_request(request), instance=salary)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your salary income has been updated!')
            return redirect('income')
        else:
            error_dictionary = form.errors
            form = SalaryForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')

    else:
        form = SalaryForm(instance=salary)

    set_form_initial_value(form.initial)

    context = {
        'title': 'Salary',
        'form': form,
        'info': True if info == 'True' else False
    }

    return render(request, 'taxlover/salary-info.html', context)


@login_required
def salary_delete(request, pk):
    if request.method == 'POST':
        Salary.objects.filter(id=pk).delete()
        latest_income = create_or_get_current_income_obj(request.user.id)
        latest_income.salary = None
        latest_income.save()

    return redirect('income')


@login_required
def other_income_delete(request, pk):
    if request.method == 'POST':
        OtherIncome.objects.filter(id=pk).delete()
        latest_income = create_or_get_current_income_obj(request.user.id)
        latest_income.other_sources = None
        latest_income.save()

    return redirect('income')


@login_required
def tax_rebate_delete(request, pk):
    if request.method == 'POST':
        TaxRebate.objects.filter(id=pk).delete()
        latest_income = create_or_get_current_income_obj(request.user.id)
        latest_income.tax_rebate = None
        latest_income.save()

    return redirect('income')


@login_required
def tax_deduction_at_source_delete(request):
    if request.method == 'POST':
        deduction_id = 0
        if request.POST['deduction_id_for_delete'] != '':
            deduction_id = int(request.POST['deduction_id_for_delete'])
        if deduction_id > 0:
            DeductionAtSource.objects.filter(id=deduction_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = DeductionAtSource.objects.filter(tax_payer_id=request.user.id,
                                                     financial_year_beg=financial_year_beg,
                                                     financial_year_end=financial_year_end).count()

            if count == 0:
                latest_income = create_or_get_current_income_obj(request.user.id)
                latest_income.tax_deducted_at_source = None
                latest_income.save()

    return redirect('income')


@login_required
def advance_paid_tax_delete(request):
    if request.method == 'POST':
        advance_paid_id = 0
        if request.POST['advance_paid_tax_id_for_delete'] != '':
            advance_paid_id = int(request.POST['advance_paid_tax_id_for_delete'])
        if advance_paid_id > 0:
            AdvanceTax.objects.filter(id=advance_paid_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = AdvanceTax.objects.filter(tax_payer_id=request.user.id,
                                              financial_year_beg=financial_year_beg,
                                              financial_year_end=financial_year_end).count()

            if count == 0:
                latest_income = create_or_get_current_income_obj(request.user.id)
                latest_income.advance_paid_tax = None
                latest_income.save()

    return redirect('income')


@login_required
def tax_refund_delete(request, pk):
    if request.method == 'POST':
        TaxRefund.objects.filter(id=pk).delete()
        latest_income = create_or_get_current_income_obj(request.user.id)
        latest_income.adjustment_of_tax_refund = None
        latest_income.save()

    return redirect('income')


@login_required
def agricultural_property_delete(request):
    if request.method == 'POST':
        agricultural_property_id = 0
        if request.POST['agricultural_property_id_for_delete'] != '':
            agricultural_property_id = int(request.POST['agricultural_property_id_for_delete'])
        if agricultural_property_id > 0:
            AgriculturalProperty.objects.filter(id=agricultural_property_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = AgriculturalProperty.objects.filter(tax_payer_id=request.user.id,
                                                        financial_year_beg=financial_year_beg,
                                                        financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.agricultural_property = None
                latest_assets.save()

    return redirect('assets')


@login_required
def furniture_delete(request):
    if request.method == 'POST':
        furniture_id = 0
        if request.POST['furniture_id_for_delete'] != '':
            furniture_id = int(request.POST['furniture_id_for_delete'])
        if furniture_id > 0:
            Furniture.objects.filter(id=furniture_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = Furniture.objects.filter(tax_payer_id=request.user.id,
                                             financial_year_beg=financial_year_beg,
                                             financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.furniture = None
                latest_assets.save()

    return redirect('assets')


@login_required
def jewellery_delete(request):
    if request.method == 'POST':
        jewellery_id = 0
        if request.POST['jewellery_id_for_delete'] != '':
            jewellery_id = int(request.POST['jewellery_id_for_delete'])
        if jewellery_id > 0:
            Jewellery.objects.filter(id=jewellery_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = Jewellery.objects.filter(tax_payer_id=request.user.id,
                                             financial_year_beg=financial_year_beg,
                                             financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.jewellery = None
                latest_assets.save()

    return redirect('assets')


@login_required
def electronic_equipment_delete(request):
    if request.method == 'POST':
        electronic_equipment_id = 0
        if request.POST['electronic_equipment_id_for_delete'] != '':
            electronic_equipment_id = int(request.POST['electronic_equipment_id_for_delete'])
        if electronic_equipment_id > 0:
            ElectronicEquipment.objects.filter(id=electronic_equipment_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = ElectronicEquipment.objects.filter(tax_payer_id=request.user.id,
                                                       financial_year_beg=financial_year_beg,
                                                       financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.electronic_equipment = None
                latest_assets.save()

    return redirect('assets')


@login_required
def cash_assets_delete(request, pk):
    if request.method == 'POST':
        CashAssets.objects.filter(id=pk).delete()
        latest_assets = create_or_get_current_assets_obj(request.user.id)
        latest_assets.cash_assets = None
        latest_assets.save()

    return redirect('assets')


@login_required
def other_assets_delete(request):
    if request.method == 'POST':
        other_assets_id = 0
        if request.POST['other_assets_id_for_delete'] != '':
            other_assets_id = int(request.POST['other_assets_id_for_delete'])
        if other_assets_id > 0:
            OtherAssets.objects.filter(id=other_assets_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = OtherAssets.objects.filter(tax_payer_id=request.user.id,
                                               financial_year_beg=financial_year_beg,
                                               financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.other_assets = None
                latest_assets.save()

    return redirect('assets')


@login_required
def other_assets_receipt_delete(request):
    if request.method == 'POST':
        other_assets_receipt_id = 0
        if request.POST['other_assets_receipt_id_for_delete'] != '':
            other_assets_receipt_id = int(request.POST['other_assets_receipt_id_for_delete'])
        if other_assets_receipt_id > 0:
            OtherAssetsReceipt.objects.filter(id=other_assets_receipt_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = OtherAssetsReceipt.objects.filter(tax_payer_id=request.user.id,
                                                      financial_year_beg=financial_year_beg,
                                                      financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.other_assets_receipt = None
                latest_assets.save()

    return redirect('assets')


@login_required
def previous_year_net_wealth_delete(request, pk):
    if request.method == 'POST':
        PreviousYearNetWealth.objects.filter(id=pk).delete()
        latest_assets = create_or_get_current_assets_obj(request.user.id)
        latest_assets.previous_year_net_wealth = None
        latest_assets.save()

    return redirect('assets')


@login_required
def upload_salary_statement(request):
    if request.method == 'POST':
        tax_payer = create_or_get_tax_payer_obj(request.user.id)
        form = UploadSalaryStatementForm(request.POST, request.FILES)
        if form.is_valid():
            income_year_beg, income_year_end = get_income_years()
            try:
                Document.objects.get(tax_payer_id=request.user.id,
                                     income_year_beg=income_year_beg,
                                     income_year_end=income_year_end)
                response_data = {'has_salary_document': True}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except Document.DoesNotExist:
                try:
                    Salary.objects.get(tax_payer_id=request.user.id,
                                       financial_year_beg=income_year_beg,
                                       financial_year_end=income_year_end)
                except Salary.DoesNotExist:
                    salary_statement_document = Document(file=request.FILES['file'])
                    salary_statement_document.tax_payer_id = tax_payer.id
                    salary_statement_document.income_year_beg = income_year_beg
                    salary_statement_document.income_year_end = income_year_end
                    salary_statement_document.document_name = "Salary Statement"
                    salary_statement_document.description = "Evaluated for {} - {} salary income.".format(
                        income_year_beg,
                        income_year_end)
                    salary_statement_document.save()

                    total_annual_payment = process_and_save_salary(salary_statement_document, request.user.id)
                    has_total_annual_payment = False
                    if total_annual_payment > 0:
                        salary_statement_document.save()
                        has_total_annual_payment = True
                    else:
                        Document.delete(salary_statement_document)

                    response_data = {'has_total_annual_payment': has_total_annual_payment}
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        form = UploadSalaryStatementForm()

    context = {
        'title': 'Income',
        'form': form
    }

    return render(request, 'taxlover/upload-salary-statement.html', context)


@login_required
def other_income(request):
    other_income_obj = get_current_financial_year_other_income_by_payer(request.user.id)
    if not other_income_obj:
        financial_year_beg, financial_year_end = get_income_years()
        other_income_obj = OtherIncome(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                       financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = OtherIncomeForm(copy_request(request), instance=other_income_obj)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your other income has been updated!')
            return redirect('income')
        else:
            error_dictionary = form.errors
            form = SalaryForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')

    else:
        form = OtherIncomeForm(instance=other_income_obj)

    set_form_initial_value(form.initial)

    context = {
        'title': 'Other Income',
        'form': form
    }

    return render(request, 'taxlover/other-income.html', context)


@login_required
def tax_rebate(request):
    tax_rebate_obj = get_current_financial_year_tax_rebate_by_payer(request.user.id)
    if not tax_rebate_obj:
        financial_year_beg, financial_year_end = get_income_years()
        tax_rebate_obj = TaxRebate(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                   financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = TaxRebateForm(copy_request(request), instance=tax_rebate_obj)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your tax rebate has been updated!')
            return redirect('income')
        else:
            error_dictionary = form.errors
            form = TaxRebateForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')

    else:
        form = TaxRebateForm(instance=tax_rebate_obj)

    if not form.initial['self_and_employers_contribution_to_pf']:
        salary = get_current_financial_year_salary_by_payer(request.user.id)
        if salary and salary.get_employers_contribution_to_pf > 0:
            form.initial['self_and_employers_contribution_to_pf'] = salary.get_employers_contribution_to_pf * 2

    set_form_initial_value(form.initial)

    context = {
        'title': 'Tax Rebate',
        'form': form
    }

    return render(request, 'taxlover/tax-rebate.html', context)


@login_required
def save_tax_deduction_at_source(request):
    if request.method == 'POST':
        financial_year_beg, financial_year_end = get_income_years()
        deduction_id = 0
        if request.POST['deduction_id'] != '':
            deduction_id = int(request.POST['deduction_id'])

        if deduction_id > 0:
            deduction_at_source = DeductionAtSource.objects.get(pk=deduction_id)
        else:
            deduction_at_source = DeductionAtSource(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                                    financial_year_end=financial_year_end)
        das_form = DeductionAtSourceForm(copy_request(request), instance=deduction_at_source)

        if das_form.is_valid():
            das_form.save()
            messages.success(request, f'Tax deduction at source added!')
            return redirect('income')
        else:
            error_dictionary = das_form.errors
            das_form = DeductionAtSourceForm(request.POST)
            set_form_validation_errors(error_dictionary, das_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')

        income_dto = IncomeDTO(request.user.id, False)
        atp_form = AdvanceTaxPaidForm(request.POST)

        context = {
            'income_dto': income_dto,
            'title': 'Income',
            'das_form': das_form,
            'atp_form': atp_form
        }

        return render(request, 'taxlover/income.html', context)


@login_required
def save_advance_paid_tax(request):
    if request.method == 'POST':
        financial_year_beg, financial_year_end = get_income_years()
        advance_paid_tax_id = 0
        if request.POST['advance_paid_tax_id'] != '':
            advance_paid_tax_id = int(request.POST['advance_paid_tax_id'])

        if advance_paid_tax_id > 0:
            advance_paid_tax = AdvanceTax.objects.get(pk=advance_paid_tax_id)
        else:
            advance_paid_tax = AdvanceTax(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                          financial_year_end=financial_year_end)
        atp_form = AdvanceTaxPaidForm(copy_request(request), instance=advance_paid_tax)

        if atp_form.is_valid():
            atp_form.save()
            messages.success(request, f'Advance paid tax added!')
            return redirect('income')
        else:
            error_dictionary = atp_form.errors
            apt_form = AdvanceTaxPaidForm(request.POST)
            set_form_validation_errors(error_dictionary, apt_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')

        income_dto = IncomeDTO(request.user.id, False)
        das_form = DeductionAtSourceForm(request.POST)

        context = {
            'income_dto': income_dto,
            'title': 'Income',
            'das_form': das_form,
            'atp_form': atp_form
        }

        return render(request, 'taxlover/income.html', context)


@login_required
def save_tax_refund(request):
    tax_refund_obj = get_current_financial_year_tax_refund_by_payer(request.user.id)
    if not tax_refund_obj:
        financial_year_beg, financial_year_end = get_income_years()
        tax_refund_obj = TaxRefund(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                   financial_year_end=financial_year_end)

    has_error = False
    if request.method == 'POST':
        tr_form = TaxRefundForm(copy_request(request), instance=tax_refund_obj)

        if tr_form.is_valid():
            tr_form.save()
            messages.success(request, f'Tax refund added!')
            return redirect('income')
        else:
            error_dictionary = tr_form.errors
            tr_form = TaxRefundForm(request.POST)
            set_form_validation_errors(error_dictionary, tr_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        income_dto = IncomeDTO(request.user.id, has_error)
        das_form = DeductionAtSourceForm(request.POST)
        atp_form = AdvanceTaxPaidForm(request.POST)

        context = {
            'income_dto': income_dto,
            'title': 'Income',
            'das_form': das_form,
            'atp_form': atp_form,
            'tr_form': tr_form
        }

        return render(request, 'taxlover/income.html', context)


@login_required
def save_agricultural_property(request):
    if request.method == 'POST':
        message = f'Agricultural property added!'
        financial_year_beg, financial_year_end = get_income_years()
        agricultural_property_id = 0
        if request.POST['agricultural_property_id'] != '':
            agricultural_property_id = int(request.POST['agricultural_property_id'])

        if agricultural_property_id > 0:
            agricultural_property = AgriculturalProperty.objects.get(pk=agricultural_property_id)
            message = f'Agricultural property updated!'
        else:
            agricultural_property = AgriculturalProperty(tax_payer_id=request.user.id,
                                                         financial_year_beg=financial_year_beg,
                                                         financial_year_end=financial_year_end)
        ap_form = AgriculturalPropertyForm(copy_request(request), instance=agricultural_property)

        if ap_form.is_valid():
            ap_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = ap_form.errors
            ap_form = AgriculturalPropertyForm(request.POST)
            set_form_validation_errors(error_dictionary, ap_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        f_form = FurnitureForm(request.POST)
        j_form = JewelleryForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_furniture(request):
    if request.method == 'POST':
        message = f'Furniture added!'
        financial_year_beg, financial_year_end = get_income_years()
        furniture_id = 0
        if request.POST['furniture_id'] != '':
            furniture_id = int(request.POST['furniture_id'])

        if furniture_id > 0:
            furniture = Furniture.objects.get(pk=furniture_id)
            message = f'Furniture updated!'
        else:
            furniture = Furniture(tax_payer_id=request.user.id,
                                                         financial_year_beg=financial_year_beg,
                                                         financial_year_end=financial_year_end)
        f_form = FurnitureForm(copy_request(request), instance=furniture)

        if f_form.is_valid():
            f_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = f_form.errors
            f_form = FurnitureForm(request.POST)
            set_form_validation_errors(error_dictionary, f_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        j_form = JewelleryForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_jewellery(request):
    if request.method == 'POST':
        message = f'Jewellery added!'
        financial_year_beg, financial_year_end = get_income_years()
        jewellery_id = 0
        if request.POST['jewellery_id'] != '':
            jewellery_id = int(request.POST['jewellery_id'])

        if jewellery_id > 0:
            jewellery = Jewellery.objects.get(pk=jewellery_id)
            message = f'Jewellery updated!'
        else:
            jewellery = Jewellery(tax_payer_id=request.user.id,
                                                         financial_year_beg=financial_year_beg,
                                                         financial_year_end=financial_year_end)
        j_form = JewelleryForm(copy_request(request), instance=jewellery)

        if j_form.is_valid():
            j_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = j_form.errors
            j_form = JewelleryForm(request.POST)
            set_form_validation_errors(error_dictionary, j_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        f_form = FurnitureForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_electronic_equipment(request):
    if request.method == 'POST':
        message = f'Electronic Equipment added!'
        financial_year_beg, financial_year_end = get_income_years()
        electronic_equipment_id = 0
        if request.POST['electronic_equipment_id'] != '':
            electronic_equipment_id = int(request.POST['electronic_equipment_id'])

        if electronic_equipment_id > 0:
            electronic_equipment = ElectronicEquipment.objects.get(pk=electronic_equipment_id)
            message = f'Electronic Equipment updated!'
        else:
            electronic_equipment = ElectronicEquipment(tax_payer_id=request.user.id,
                                                         financial_year_beg=financial_year_beg,
                                                         financial_year_end=financial_year_end)
        ee_form = ElectronicEquipmentForm(copy_request(request), instance=electronic_equipment)

        if ee_form.is_valid():
            ee_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = ee_form.errors
            ee_form = ElectronicEquipmentForm(request.POST)
            set_form_validation_errors(error_dictionary, ee_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        f_form = FurnitureForm(request.POST)
        j_form = JewelleryForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_cash_assets(request):
    cash_assets = get_current_financial_year_cash_assets_by_payer(request.user.id)
    if not cash_assets:
        financial_year_beg, financial_year_end = get_income_years()
        cash_assets = CashAssets(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                 financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = CashAssetsForm(copy_request(request), instance=cash_assets)

        if form.is_valid():
            form.save()
            messages.success(request, f'Cash assets has been updated!')
            return redirect('assets')
        else:
            error_dictionary = form.errors
            form = CashAssetsForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
    else:
        form = CashAssetsForm(instance=cash_assets)

        set_form_initial_value(form.initial)

        context = {
            'title': 'Cash Assets',
            'form': form
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_other_assets(request):
    if request.method == 'POST':
        message = f'Other Assets added!'
        financial_year_beg, financial_year_end = get_income_years()
        other_assets_id = 0
        if request.POST['other_assets_id'] != '':
            other_assets_id = int(request.POST['other_assets_id'])

        if other_assets_id > 0:
            other_assets = OtherAssets.objects.get(pk=other_assets_id)
            message = f'Other Assets updated!'
        else:
            other_assets = OtherAssets(tax_payer_id=request.user.id,
                                       financial_year_beg=financial_year_beg,
                                       financial_year_end=financial_year_end)
        oa_form = OtherAssetsForm(copy_request(request), instance=other_assets)

        if oa_form.is_valid():
            oa_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = oa_form.errors
            oa_form = OtherAssetsForm(request.POST)
            set_form_validation_errors(error_dictionary, oa_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        f_form = FurnitureForm(request.POST)
        j_form = JewelleryForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_other_assets_receipt(request):
    if request.method == 'POST':
        message = f'Other Assets Receipt added!'
        financial_year_beg, financial_year_end = get_income_years()
        other_assets_receipt_id = 0
        if request.POST['other_assets_receipt_id'] != '':
            other_assets_receipt_id = int(request.POST['other_assets_receipt_id'])

        if other_assets_receipt_id > 0:
            other_assets_receipt = OtherAssetsReceipt.objects.get(pk=other_assets_receipt_id)
            message = f'Other Assets Receipts updated!'
        else:
            other_assets_receipt = OtherAssetsReceipt(tax_payer_id=request.user.id,
                                                      financial_year_beg=financial_year_beg,
                                                      financial_year_end=financial_year_end)
        oar_form = OtherAssetsReceiptForm(copy_request(request), instance=other_assets_receipt)

        if oar_form.is_valid():
            oar_form.save()
            messages.success(request, message)
            return redirect('assets')
        else:
            error_dictionary = oar_form.errors
            oar_form = OtherAssetsReceiptForm(request.POST)
            set_form_validation_errors(error_dictionary, oar_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        f_form = FurnitureForm(request.POST)
        j_form = JewelleryForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        pynw_form = PreviousYearNetWealthForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def save_previous_year_net_wealth(request):
    previous_year_net_wealth = get_current_financial_year_previous_year_net_wealth_receipt_by_payer(request.user.id)
    if not previous_year_net_wealth:
        financial_year_beg, financial_year_end = get_income_years()
        previous_year_net_wealth = PreviousYearNetWealth(tax_payer_id=request.user.id,
                                                         financial_year_beg=financial_year_beg,
                                                         financial_year_end=financial_year_end)

    has_error = False
    if request.method == 'POST':
        pynw_form = PreviousYearNetWealthForm(copy_request(request), instance=previous_year_net_wealth)

        if pynw_form.is_valid():
            pynw_form.save()
            messages.success(request, f'Previous year net wealth added!')
            return redirect('assets')
        else:
            error_dictionary = pynw_form.errors
            pynw_form = OtherAssetsReceiptForm(request.POST)
            set_form_validation_errors(error_dictionary, pynw_form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_error = True

        assets_dto = AssetsDTO(request.user.id, has_error)
        ap_form = AgriculturalPropertyForm(request.POST)
        f_form = FurnitureForm(request.POST)
        j_form = JewelleryForm(request.POST)
        ee_form = ElectronicEquipmentForm(request.POST)
        oa_form = OtherAssetsForm(request.POST)
        oar_form = OtherAssetsReceiptForm(request.POST)

        context = {
            'assets_dto': assets_dto,
            'title': 'Assets',
            'ap_form': ap_form,
            'f_form': f_form,
            'j_form': j_form,
            'ee_form': ee_form,
            'oa_form': oa_form,
            'oar_form': oar_form,
            'pynw_form': pynw_form,
        }

        return render(request, 'taxlover/assets.html', context)


@login_required
def assets(request):
    assets_dto = AssetsDTO(request.user.id, False)

    ap_form = AgriculturalPropertyForm(request.POST)

    context = {
        'assets_dto': assets_dto,
        'ap_form': ap_form
    }

    return render(request, 'taxlover/assets.html', context)


@login_required
def save_assets_data(request, source, answer):
    latest_assets = create_or_get_current_assets_obj(request.user.id)
    show_success_message = save_assets(latest_assets, source, answer, request)

    if show_success_message:
        messages.success(request, f'Data updated successfully!')

    context = {
        'latest_assets': latest_assets,
        'title': 'Assets'
    }

    if source == 'investments':
        if latest_assets.investments:
            return redirect('investment-info', 0)
        else:
            return redirect('assets')
    if source == 'motor_vehicle':
        if latest_assets.motor_vehicle:
            return redirect('motor-vehicle-info', 0)
        else:
            return redirect('assets')
    elif source == 'business_capital' or source == 'directors_shareholding_assets' or \
            source == 'non_agricultural_property' or source == 'agricultural_property' or \
            source == 'furniture' or source == 'jewellery' or \
            source == 'electronic_equipment' or source == 'cash_assets' or \
            source == 'other_assets' or source == 'other_assets_receipt' or source == 'previous_year_net_wealth':
        return redirect('assets')


@login_required
def investment_info(request, pk):
    has_form_error = False
    financial_year_beg, financial_year_end = get_income_years()
    if pk > 0:
        investment = Investment.objects.get(pk=pk)
    else:
        investment = Investment(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = InvestmentForm(copy_request(request), instance=investment)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your investment has been updated!')
            return redirect('assets')
        else:
            error_dictionary = form.errors
            form = InvestmentForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_form_error = True

    else:
        form = InvestmentForm(instance=investment)

    if pk > 0 and not has_form_error:
        form.initial['value'] = add_comma(form.initial['value'])

    context = {
        'title': 'Investment',
        'form': form
    }

    return render(request, 'taxlover/investment-info.html', context)


@login_required
def motor_vehicle_info(request, pk):
    has_form_error = False
    financial_year_beg, financial_year_end = get_income_years()
    if pk > 0:
        motor_vehicle = MotorVehicle.objects.get(pk=pk)
    else:
        motor_vehicle = MotorVehicle(tax_payer_id=request.user.id, financial_year_beg=financial_year_beg,
                                     financial_year_end=financial_year_end)

    if request.method == 'POST':
        form = MotorVehicleForm(copy_request(request), instance=motor_vehicle)

        if form.is_valid():
            form.save()
            messages.success(request, f'Your motor vehicle has been updated!')
            return redirect('assets')
        else:
            error_dictionary = form.errors
            form = MotorVehicleForm(request.POST)
            set_form_validation_errors(error_dictionary, form.fields)
            messages.error(request, f'Please correct the errors below, and try again.')
            has_form_error = True

    else:
        form = MotorVehicleForm(instance=motor_vehicle)

    if pk > 0 and not has_form_error:
        form.initial['value'] = add_comma(form.initial['value'])

    context = {
        'title': 'Motor Vehicle',
        'form': form
    }

    return render(request, 'taxlover/motor-vehicle-info.html', context)


@login_required
def investment_delete(request):
    if request.method == 'POST':
        investment_id = 0
        if request.POST['investment_id_for_delete'] != '':
            investment_id = int(request.POST['investment_id_for_delete'])
        if investment_id > 0:
            Investment.objects.filter(id=investment_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = Investment.objects.filter(tax_payer_id=request.user.id,
                                              financial_year_beg=financial_year_beg,
                                              financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.investments = None
                latest_assets.save()

    return redirect('assets')


@login_required
def motor_vehicle_delete(request):
    if request.method == 'POST':
        motor_vehicle_id = 0
        if request.POST['motor_vehicle_id_for_delete'] != '':
            motor_vehicle_id = int(request.POST['motor_vehicle_id_for_delete'])
        if motor_vehicle_id > 0:
            MotorVehicle.objects.filter(id=motor_vehicle_id).delete()

            financial_year_beg, financial_year_end = get_income_years()
            count = MotorVehicle.objects.filter(tax_payer_id=request.user.id,
                                                financial_year_beg=financial_year_beg,
                                                financial_year_end=financial_year_end).count()

            if count == 0:
                latest_assets = create_or_get_current_assets_obj(request.user.id)
                latest_assets.motor_vehicle = None
                latest_assets.save()

    return redirect('assets')


def index(request):
    et_sess = ExtractTable(api_key='qAm4mcOR3p5qZsMk2IM9m3hXk0BF7IbR5WheMLIK')  # Replace your VALID API Key here
    print(et_sess.check_usage())  # Checks the API Key validity as well as shows associated plan usage

    # tax_payer = TaxPayer()
    # tax_payer.name = 'Md Khairul Bashar Chowdhury'
    # tax_payer.save()

    tax_payer_row = TaxPayer.objects.get(name='Md Khairul Bashar Chowdhury')

    if tax_payer_row is not None:
        salary_row = Salary.objects.filter(tax_payer=tax_payer_row)
        if len(salary_row) == 0:
            # salary_table_data = et_sess.process_file(filepath='samples/sample_salary_cert.jpg', output_format="df")

            json_str = '{"0":{"0":"Description","1":"Basic Salary","2":"Perquisite:","3":"(a) House Rent allowance","4":"(b) Medical allowance","5":"(c) ' \
                       'Conveyance allowance","6":"(d) Leave fare assistance","7":"Total Perquisite","8":"Bonuses:","9":"(a) Festival Bonus","10":"(b) ' \
                       'Other Bonuses","11":"Total Bonuses","12":"Provident Fund:","13":"(a) Employer\'s contribution to PF","14":"(b) Employee\'s contribution to PF",' \
                       '"15":"Total CPF","16":"Total Annual Payment","17":"Deductions:","18":"Deducted & deposited of CPF (Both contribution)","19":"Advance Income Tax ' \
                       'deposited (Challan"},"1":{"0":"","1":"","2":"","3":"300,000.00","4":"66,240.00","5":"30,000.00","6":"66,240.00","7":"462,480.00","8":"","9":"103,200.00",' \
                       '"10":"24,120.00","11":"127,320.00","12":"","13":"41,472.00","14":"41,472.00","15":"82,944.00","16":"","17":"","18":"","19":"enclosed)"},"2":{"0":"Amount (Tk.)",' \
                       '"1":"662,400.00","2":"","3":"","4":"","5":"","6":"","7":"462,480.00","8":"","9":"","10":"","11":"127,320.00","12":"","13":"","14":"","15":"41,472.00",' \
                       '"16":"1,293,672.00","17":"","18":"82,944.00","19":"24,000.00"}}'

            json_obj = json.loads(json_str)
            salary_table_data = pd.DataFrame(data=json_obj)
            table_column_length = len(salary_table_data.columns)
            salary = Salary()
            salary.tax_payer_id = tax_payer_row.id

            # for row_index, row in salary_table_data.iterrows():
            #     print(row[0])
            #     salary_category = str(row[0]).lower()
            #     if 'basic' in salary_category:
            #         salary.basic = parse_data(row, table_column_length)
            #     elif 'house rent' in salary_category:
            #         salary.house_rent = parse_data(row, table_column_length)
            #     elif 'medical' in salary_category:
            #         salary.medical = parse_data(row, table_column_length)
            #     elif 'conveyance' in salary_category:
            #         salary.conveyance = parse_data(row, table_column_length)
            #     elif 'leave fare assistance' in salary_category:
            #         salary.lfa = parse_data(row, table_column_length)
            #     elif 'festival bonus' in salary_category:
            #         salary.festival_bonus = parse_data(row, table_column_length)
            #     elif 'other bonus' in salary_category:
            #         salary.other_bonus = parse_data(row, table_column_length)
            #     elif 'employer\'s contribution to pf' in salary_category:
            #         salary.employers_contribution_to_pf = parse_data(row, table_column_length)
            #     elif 'employee\'s contribution to pf' in salary_category:
            #         salary.employees_contribution_to_pf = parse_data(row, table_column_length)
            #     elif 'advance income tax' in salary_category:
            #         salary.ait = parse_data(row, table_column_length)

            salary.financial_year_beg = 2019
            salary.financial_year_end = 2020

            salary.save()

    return HttpResponse(salary_row)


def generate_old(request):
    # canvas = Canvas("hello.pdf")
    # width, height = A4
    # canvas.drawCentredString(72, 72, "Hello, World")
    # canvas.drawCentredString(800, 600, "Hello, World")
    # canvas.drawCentredString(2.75 * inch, 1.3 * inch, "SPUMONI")
    # canvas.save()

    # html = '<!DOCTYPE html><html><body><h2>HTML Images</h2><p>HTML images are defined with the img tag:</p><img src="w3schools.jpg" alt="W3Schools.com" width="104" height="142"></body></html>'

    # pdfkit.from_file('editables/test.html', 'sample.pdf')
    # pdfkit.from_file('editables/94.html', 'sample.pdf')
    # pdfkit.from_string(html, 'sample.pdf')

    # html = "<h1>Hello World !!!</h1>"
    # static_path = "editables/"
    # file_path = "out.pdf"
    # generate_pdf(html, static_path, file_path)

    # HTML('http://weasyprint.org/').write_pdf('/output/weasyprint-website.pdf')

    return HttpResponse('ok')


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


@login_required(login_url='/admin/login/')
def generate(request):
    tax_payer = TaxPayer.objects.get(user_id=request.user.id)
    tax_payer_dto = TaxPayerDTO(tax_payer)
    context = {
        'tax_payer': tax_payer_dto,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template('taxlover/return-form.html')
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def download_return(request):
    context = {
        'title': 'Download Return'
    }
    return render(request, 'taxlover/download-return.html', context)


@login_required
def get_category_wise_exempted_value(request):
    if request.is_ajax() and request.method == 'GET':
        category = request.GET['category']
        data = {}

        if category == 'house_rent':
            basic = request.GET['basic']
            house_rent = request.GET['house_rent']

            data = {
                'house_rent_exempted': get_house_rent_exempted(basic, house_rent)
            }
        elif category == 'medical':
            basic = request.GET['basic']
            medical = request.GET['medical']

            data = {
                'medical_exempted': get_medical_exempted(basic, medical)
            }
        elif category == 'conveyance':
            conveyance = request.GET['conveyance']

            data = {
                'conveyance_exempted': get_conveyance_exempted(conveyance)
            }
        elif category == 'interest_from_mutual_fund_unit_fund':
            interest_from_mutual_fund = request.GET['interest_from_mutual_fund_unit_fund']

            data = {
                'interest_from_mutual_fund_unit_fund_exempted': get_interest_from_mutual_fund_exempted(
                    interest_from_mutual_fund)
            }
        elif category == 'cash_dividend_from_company_listed_in_stock_exchange':
            cash_dividend = request.GET['cash_dividend_from_company_listed_in_stock_exchange']

            data = {
                'cash_dividend_from_company_listed_in_stock_exchange_exempted': get_cash_dividend_exempted(
                    cash_dividend)
            }

        return JsonResponse(data)


@login_required
def get_category_wise_allowed_investment_value(request):
    if request.is_ajax() and request.method == 'GET':
        category = request.GET['category']
        data = {}

        if category == 'life_insurance_premium':
            life_insurance_premium = request.GET['life_insurance_premium']
            life_insurance_premium_policy_value = request.GET['life_insurance_premium_policy_value']

            data = {
                'life_insurance_premium_allowed': get_life_insurance_premium_allowed(life_insurance_premium,
                                                                                     life_insurance_premium_policy_value)
            }
        elif category == 'contribution_to_dps':
            contribution_to_dps = request.GET['contribution_to_dps']

            data = {
                'contribution_to_dps_allowed': get_contribution_to_dps_allowed(contribution_to_dps)
            }

        return JsonResponse(data)


@login_required
def get_data_for_edit(request):
    if request.is_ajax() and request.method == 'GET':
        section = request.GET['section']
        data_id = request.GET['id']
        data = {}

        if section == 'deduction_at_source':
            deduction_at_source = DeductionAtSource.objects.get(pk=data_id)
            data = {
                'id': deduction_at_source.id,
                'description': deduction_at_source.description,
                'tax_deducted_at_source': deduction_at_source.tax_deducted_at_source
            }
        elif section == 'advance_tax_paid':
            advance_tax = AdvanceTax.objects.get(pk=data_id)
            data = {
                'id': advance_tax.id,
                'type': advance_tax.type,
                'description': advance_tax.description,
                'advance_paid_tax': advance_tax.advance_paid_tax
            }
        elif section == 'agricultural_property':
            agricultural_property = AgriculturalProperty.objects.get(pk=data_id)
            data = {
                'id': agricultural_property.id,
                'description': agricultural_property.description,
                'value': agricultural_property.value
            }

        return JsonResponse(data)
