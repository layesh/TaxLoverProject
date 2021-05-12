from django.urls import path
from .views import (
    SalaryListView,
    SalaryDetailView,
    SalaryCreateView,
    SalaryUpdateView,
    SalaryDeleteView
)
from . import views

urlpatterns = [
    # path('', views.home, name='tax-lover-home'),
    path('', SalaryListView.as_view(), name='tax-lover-home'),
    path('salary/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),
    path('salary/new/', SalaryCreateView.as_view(), name='salary-create'),
    path('salary/<int:pk>/update/', SalaryUpdateView.as_view(), name='salary-update'),
    path('salary/<int:pk>/delete/', SalaryDeleteView.as_view(), name='salary-delete'),
    path('about/', views.about, name='tax-lover-about'),
    path('generate/', views.generate, name='generate')
]

