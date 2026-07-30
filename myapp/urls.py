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
    # Home
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
    'calendar/',
    views.Calender,
    name="calendar"
),


path(
    'add-event/',
    views.add_event,
    name="add_event"
),


    # ==========================
    # PDF Downloads
    # ==========================

    path(
        "download-expense-pdf/",
        views.download_expense_pdf,
        name="download_pdf"
    ),


    path(
        "download-earning-pdf/",
        views.download_earnings_pdf,
        name="download_earning_pdf"
    ),


    # ==========================
    # Clear Data
    # ==========================

    path(
        "clear-all-data/",
        views.clear_all_data,
        name="clear_all_data"
    ),



    # ==========================
    # Custom Admin Dashboard
    # ==========================

    path(
        "adminpage/",
        views.adminpage,
        name="adminpage"
    ),


    # ==========================
    # Admin Expense
    # ==========================

    path(
        "adminpage/add-expense/<int:user_id>/",
        views.admin_add_expense,
        name="admin_add_expense"
    ),


    path(
        "adminpage/update-expense/<int:expense_id>/",
        views.admin_update_expense,
        name="admin_update_expense"
    ),


    path(
        "adminpage/delete-expense/<int:expense_id>/",
        views.admin_delete_expense,
        name="admin_delete_expense"
    ),



    # ==========================
    # Admin Earnings
    # ==========================

    path(
        "adminpage/add-earning/<int:user_id>/",
        views.admin_add_earning,
        name="admin_add_earning"
    ),


    path(
        "adminpage/update-earning/<int:earning_id>/",
        views.admin_update_earning,
        name="admin_update_earning"
    ),


    path(
        "adminpage/delete-earning/<int:earning_id>/",
        views.admin_delete_earning,
        name="admin_delete_earning"
    ),



    # ==========================
    # Admin Notes
    # ==========================

    path(
        "adminpage/add-note/<int:user_id>/",
        views.admin_add_note,
        name="admin_add_note"
    ),


    path(
        "adminpage/update-note/<int:note_id>/",
        views.admin_update_note,
        name="admin_update_note"
    ),


    path(
        "adminpage/delete-note/<int:note_id>/",
        views.admin_delete_note,
        name="admin_delete_note"
    ),

]