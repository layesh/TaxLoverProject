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
    path('generate/', views.generate, name='generate'),
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
]
