from django.conf.urls import url
from django.urls import path
from .views import (
    SalaryListView,
    SalaryDetailView,
    SalaryCreateView,
    SalaryUpdateView,
    SalaryDeleteView
)
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.home, name='login'),
    path('', user_views.login_view, name='login'),
    # path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('dashboard', SalaryListView.as_view(extra_context={'title': 'Dashboard'}), name='dashboard'),
    path('dashboard', views.home, name='dashboard'),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),
    path('salary/new/', SalaryCreateView.as_view(), name='salary-create'),
    path('salary/<int:pk>/update/', SalaryUpdateView.as_view(), name='salary-update'),
    # path('salary/<int:pk>/delete/', SalaryDeleteView.as_view(), name='salary-delete'),
    path('personal-info/', views.personal_info, name='personal-info'),
    path('income/', views.income, name='income'),
    path('assets/', views.assets, name='assets'),
    path('confirm-assets-copy/', views.confirm_assets_copy, name='confirm-assets-copy'),
    path('generate/<str:submit_under_82bb>', views.generate, name='generate'),
    path('download-return/', views.download_return, name='download-return'),
    path('save-income-data/<str:source>/<str:answer>/', views.save_income_data, name='save-income-data'),
    path('salary-info/', views.salary_info, name='salary-info'),
    path('salary-delete/<int:pk>/', views.salary_delete, name='salary-delete'),
    path('upload-salary-statement/', views.upload_salary_statement, name='upload-salary-statement'),
    path('get_category_wise_exempted_value/', views.get_category_wise_exempted_value,
         name='get_category_wise_exempted_value'),
    path('other-income/', views.other_income, name='other-income'),
    path('other_income-delete/<int:pk>/', views.other_income_delete, name='other_income_delete'),
    path('tax_rebate/', views.tax_rebate, name='tax_rebate'),
    path('get_category_wise_allowed_investment_value/', views.get_category_wise_allowed_investment_value,
         name='get_category_wise_allowed_investment_value'),
    path('tax_rebate_delete/<int:pk>/', views.tax_rebate_delete, name='tax_rebate_delete'),
    path('save-tax-deduction-at-source/', views.save_tax_deduction_at_source, name='save-tax-deduction-at-source'),
    path('get-data-for-edit/', views.get_data_for_edit, name='get-data-for-edit'),
    path('tax-deduction-at-source-delete/', views.tax_deduction_at_source_delete,
         name='tax-deduction-at-source-delete'),
    path('advance-paid-tax-delete/', views.advance_paid_tax_delete,
         name='advance-paid-tax-delete'),
    path('save-advance-paid-tax/', views.save_advance_paid_tax, name='save-advance-paid-tax'),
    path('save-tax-refund/', views.save_tax_refund, name='save-tax-refund'),
    path('tax-refund-delete/<int:pk>/', views.tax_refund_delete, name='tax-refund-delete'),
    path('save-assets-data/<str:source>/<str:answer>/', views.save_assets_data, name='save-assets-data'),
    path('agricultural-property-delete/', views.agricultural_property_delete,
         name='agricultural-property-delete'),
    path('save-agricultural-property/', views.save_agricultural_property, name='save-agricultural-property'),
    path('investment-info/<int:pk>/', views.investment_info, name='investment-info'),
    path('investment-delete/', views.investment_delete,
         name='investment-delete'),
    path('motor-vehicle-info/<int:pk>/', views.motor_vehicle_info, name='motor-vehicle-info'),
    path('motor-vehicle-delete/', views.motor_vehicle_delete,
         name='motor-vehicle-delete'),
    path('save-furniture/', views.save_furniture, name='save-furniture'),
    path('furniture-delete/', views.furniture_delete,
         name='furniture-delete'),
    path('save-jewellery/', views.save_jewellery, name='save-jewellery'),
    path('jewellery-delete/', views.jewellery_delete,
         name='jewellery-delete'),
    path('save-electronic-equipment/', views.save_electronic_equipment, name='save-electronic-equipment'),
    path('electronic-equipment-delete/', views.electronic_equipment_delete,
         name='electronic-equipment-delete'),
    path('cash-assets/', views.cash_assets, name='cash-assets'),
    path('cash-assets-delete/<int:pk>/', views.cash_assets_delete,
         name='cash-assets-delete'),
    path('save-other-assets/', views.save_other_assets, name='save-other-assets'),
    path('other-assets-delete/', views.other_assets_delete,
         name='other-assets-delete'),
    path('save-other-assets-receipt/', views.save_other_assets_receipt, name='save-other-assets-receipt'),
    path('other-assets-receipt-delete/', views.other_assets_receipt_delete,
         name='other-assets-receipt-delete'),
    path('save-previous-year-net-wealth/', views.save_previous_year_net_wealth, name='save-previous-year-net-wealth'),
    path('previous-year-net-wealth-delete/<int:pk>/', views.previous_year_net_wealth_delete,
         name='previous-year-net-wealth-delete'),
    path('liabilities/', views.liabilities, name='liabilities'),
    path('save-liabilities-data/<str:source>/<str:answer>/', views.save_liabilities_data, name='save-liabilities-data'),
    path('mortgage-delete/', views.mortgage_delete, name='mortgage-delete'),
    path('save-mortgage/', views.save_mortgage, name='save-mortgage'),
    path('unsecured-loan-delete/', views.unsecured_loan_delete, name='unsecured-loan-delete'),
    path('save-unsecured-loan/', views.save_unsecured_loan, name='save-unsecured-loan'),
    path('bank-loan-delete/', views.bank_loan_delete, name='bank-loan-delete'),
    path('save-bank-loan/', views.save_bank_loan, name='save-bank-loan'),
    path('other-liability-delete/', views.other_liability_delete, name='other-liability-delete'),
    path('save-other-liability/', views.save_other_liability, name='save-other-liability'),
    path('expenses/', views.expenses, name='expenses'),
    path('adjust-cash-in-hand/', views.adjust_cash_in_hand,
         name='adjust-cash-in-hand'),
    path('generate-assets-data', views.generate_assets_data,
         name='generate-assets-data'),
    path('copy-assets-data', views.copy_assets_data,
         name='copy-assets-data'),
]
