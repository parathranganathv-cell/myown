from django.urls import path
from . import views


urlpatterns = [

    # Home page
    path(
        "",
        views.Home,
        name="home"
    ),


    # Earnings page
    path(
        "e/",
        views.Earning,
        name="earning"
    ),


    # Expense page
    path(
        "a/",
        views.Amount,
        name="amount"
    ),


    # Notes page
    path("n/", views.mynotes, name="note"),

    # Calendar page
    path(
        "c/",
        views.Calender,
        name="calendar"
    ),


    # Download Expense PDF
    path(
        "download-expense-pdf/",
        views.download_expense_pdf,
        name="download_pdf"
    ),


    # Download Earnings PDF
    path(
    "download-earning-pdf/",
    views.download_earnings_pdf,
    name="download_earning_pdf"
),
path(
    "clear-all-data/",
    views.clear_all_data,
    name="clear_all_data"
),

]