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
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.home, name='login'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('dashboard', SalaryListView.as_view(), name='dashboard'),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),
    path('salary/new/', SalaryCreateView.as_view(), name='salary-create'),
    path('salary/<int:pk>/update/', SalaryUpdateView.as_view(), name='salary-update'),
    path('salary/<int:pk>/delete/', SalaryDeleteView.as_view(), name='salary-delete'),
    path('about/', views.about, name='tax-lover-about'),
    path('generate/', views.generate, name='generate')
]
