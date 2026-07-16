from django.urls import path
from . import views

urlpatterns = [
    path('i', views.Home, name='home'),

    path('e', views.Earning, name='earning'),

    path('a', views.Amount, name='amount'),

    path('n/', views.mynotes, name='note'),

    path('c', views.Calender, name='calendar'),

    path('download-pdf/', views.download_pdf, name='download_pdf'),
]