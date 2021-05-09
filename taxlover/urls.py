from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tax-lover-home'),
    path('about/', views.about, name='tax-lover-about'),
    path('generate/', views.generate, name='generate')
]

