from django.contrib import messages
from django.shortcuts import render

import json
import pandas as pd
import datetime

from ExtractTable import ExtractTable
from django.contrib.auth.decorators import login_required

from taxlover.dtos.taxPayerDTO import TaxPayerDTO
from taxlover.models import TaxPayer, Salary
from taxlover.utils import parse_data, create_or_get_tax_payer_obj, create_or_get_latest_income_obj, \
    get_assessment_years

import os
from django.conf import settings
from django.http import HttpResponse
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
    if request.method == 'POST':
        tax_payer = create_or_get_tax_payer_obj(request.user.id)

        tax_payer.e_tin = request.POST.get('e_tin')
        tax_payer.nid = request.POST.get('nid')
        tax_payer.dob = datetime.datetime.strptime(request.POST.get('dob'), "%d/%m/%Y").date()
        tax_payer.mobile_no = request.POST.get('contact_no')
        tax_payer.tax_circle = request.POST.get('tax_circle')
        tax_payer.tax_zone = request.POST.get('tax_zone')

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

        tax_payer.save()
        messages.success(request, f'Your personal info has been updated!')

        context = {
            'tax_payer': tax_payer,
            'title': 'Personal Info'
        }
    else:
        tax_payer = create_or_get_tax_payer_obj(request.user.id)

        context = {
            'tax_payer': tax_payer,
            'title': 'Personal Info'
        }
    return render(request, 'taxlover/personal-info.html', context)


@login_required
def income(request):
    tax_payer = create_or_get_tax_payer_obj(request.user.id)
    latest_income = create_or_get_latest_income_obj(request.user.id)

    context = {
        'tax_payer': tax_payer,
        'latest_income': latest_income,
        'title': 'Income'
    }

    return render(request, 'taxlover/income.html', context)


@login_required
def save_income_data(request, source, answer):
    latest_income = create_or_get_latest_income_obj(request.user.id)

    if source == 'salary':
        if answer == 'yes':
            latest_income.salary = True
        elif answer == 'no':
            latest_income.salary = False

    latest_income.save()
    messages.success(request, f'Data updated successfully!')

    context = {
        'latest_income': latest_income,
        'title': 'Income'
    }

    return render(request, 'taxlover/income.html', context)


@login_required
def assets(request):
    if request.method == 'POST':
        tax_payer = TaxPayer.objects.get(user_id=request.user.id)

        context = {
            'tax_payer': tax_payer,
            'title': 'Assets'
        }
    else:
        try:
            tax_payer = TaxPayer.objects.get(user_id=request.user.id)
        except TaxPayer.DoesNotExist:
            tax_payer = TaxPayer.objects.create(user_id=request.user.id)
        context = {
            'tax_payer': tax_payer,
            'title': 'Assets'
        }
    return render(request, 'taxlover/personal-info.html', context)


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

            for row_index, row in salary_table_data.iterrows():
                print(row[0])
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
                elif 'employer\'s contribution to pf' in salary_category:
                    salary.employers_contribution_to_pf = parse_data(row, table_column_length)
                elif 'employee\'s contribution to pf' in salary_category:
                    salary.employees_contribution_to_pf = parse_data(row, table_column_length)
                elif 'advance income tax' in salary_category:
                    salary.ait = parse_data(row, table_column_length)

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

