from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("a/", views.Amount, name="amount"),
    path("e/", views.Earning, name="earning"),
    path("n/", views.mynotes, name="note"),
    path("c/", views.Calender, name="calendar"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),
    path("clear-all/", views.clear_all_data, name="clear_all_data"),

]