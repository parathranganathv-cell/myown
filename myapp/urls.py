from django.urls import path
from . import views

urlpatterns = [

    # ==========================
    # Authentication
    # ==========================

    path(
        "",
        views.findex,
        name="findex"
    ),

    path(
        "login/",
        views.login_user,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),

    # ==========================
    # Home Page
    # ==========================

    path(
        "index/",
        views.Home,
        name="home"
    ),

    # ==========================
    # Earnings
    # ==========================

    path(
        "e/",
        views.Earning,
        name="earning"
    ),

    # ==========================
    # Expense
    # ==========================

    path(
        "a/",
        views.Amount,
        name="amount"
    ),

    # ==========================
    # Notes
    # ==========================

    path(
        "n/",
        views.mynotes,
        name="note"
    ),

    # ==========================
    # Calendar
    # ==========================

    path(
        "c/",
        views.Calender,
        name="calendar"
    ),

    # ==========================
    # Download Expense PDF
    # ==========================

    path(
        "download-expense-pdf/",
        views.download_expense_pdf,
        name="download_pdf"
    ),

    # ==========================
    # Download Earnings PDF
    # ==========================

    path(
        "download-earning-pdf/",
        views.download_earnings_pdf,
        name="download_earning_pdf"
    ),

    # ==========================
    # Clear All Data
    # ==========================

    path(
        "clear-all-data/",
        views.clear_all_data,
        name="clear_all_data"
    ),

]