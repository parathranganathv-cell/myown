from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.db import connection

from .models import Budget, Expense, Earnings, Note,CalendarEvent
from .utils import check_database_storage


# ==========================
# Home
# ==========================

# @login_required(login_url="login")
# def Home(request):
#     return render(request, "index.html")


# ==========================
# Expense Page
# ==========================

@login_required(login_url="login")
def Amount(request):

    # Clear Budget
    if request.method == "POST" and "clear_budget" in request.POST:

        budget, created = Budget.objects.get_or_create(
            user=request.user,
            defaults={"fixed_amount":0}
        )

        budget.fixed_amount = 0
        budget.save()

        return redirect("amount")


    # Save Budget
    if request.method == "POST" and "save_budget" in request.POST:

        fixed_amount = request.POST.get("fixed_amount")


        budget, created = Budget.objects.get_or_create(
            user=request.user,
            defaults={
                "fixed_amount":fixed_amount
            }
        )


        if not created:
            budget.fixed_amount = fixed_amount
            budget.save()


        return redirect("amount")



    # Save Expense
    if request.method == "POST" and "save_expense" in request.POST:

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")


        budget, created = Budget.objects.get_or_create(
            user=request.user,
            defaults={
                "fixed_amount":0
            }
        )


        Expense.objects.create(

            user=request.user,
            budget=budget,
            amount=amount,
            reason=reason

        )


        return redirect("amount")



    # Display Data

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")


    budget, created = Budget.objects.get_or_create(
        user=request.user,
        defaults={
            "fixed_amount":0
        }
    )


    amounts = Expense.objects.filter(
        user=request.user,
        budget=budget
    )


    if from_date:
        amounts = amounts.filter(
            created_at__date__gte=from_date
        )


    if to_date:
        amounts = amounts.filter(
            created_at__date__lte=to_date
        )


    total_amount = amounts.aggregate(
        Sum("amount")
    )["amount__sum"] or 0



    fixed_amount = budget.fixed_amount


    remaining_amount = fixed_amount - total_amount



    return render(
        request,
        "amount.html",
        {
            "amounts":amounts,
            "fixed_amount":fixed_amount,
            "remaining_amount":remaining_amount,
            "total_amount":total_amount,
            "from_date":from_date,
            "to_date":to_date,
        }
    )
# ==========================
# Earnings Page
# ==========================

@login_required(login_url="login")
def Earning(request):

    if request.method == "POST":

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")


        Earnings.objects.create(

            user=request.user,
            amount=amount,
            reason=reason

        )


        return redirect("earning")



    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")


    amounts = Earnings.objects.filter(
        user=request.user
    )


    if from_date:
        amounts = amounts.filter(
            created_at__date__gte=from_date
        )


    if to_date:
        amounts = amounts.filter(
            created_at__date__lte=to_date
        )


    total_amount = amounts.aggregate(
        Sum("amount")
    )["amount__sum"] or 0



    return render(
        request,
        "myearnings.html",
        {
            "amounts":amounts,
            "total_amount":total_amount
        }
    )

# ==========================
# Notes
# ==========================

@login_required(login_url="login")
def mynotes(request):

    if request.method == "POST":

        content = request.POST.get("content")


        if content:

            Note.objects.create(

                user=request.user,
                content=content

            )


        return redirect("note")



    notes = Note.objects.filter(
        user=request.user
    )


    return render(
        request,
        "mynotes.html",
        {
            "notes":notes
        }
    )
# ==========================
# Calendar
# ==========================
@login_required(login_url="login")
def Calender(request):

    events = CalendarEvent.objects.filter(
        user=request.user
    )


    return render(
        request,
        "calender.html",
        {
            "events":events
        }
    )

@login_required(login_url="login")
def add_event(request):

    if request.method == "POST":

        date = request.POST.get("date")

        title = request.POST.get("title")

        description = request.POST.get("description")


        CalendarEvent.objects.create(

            user=request.user,

            date=date,

            title=title,

            description=description

        )


        return redirect("calendar")


    return redirect("calendar")
# ==========================
# Download Expense PDF
# ==========================

def download_expense_pdf(request):

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # Remove invalid None values from URL
    if from_date in ["", "None", None]:
        from_date = None

    if to_date in ["", "None", None]:
        to_date = None


    # Get all expenses
    expenses = Expense.objects.all().order_by("-created_at")


    # Filter by date
    if from_date:
        expenses = expenses.filter(
            created_at__date__gte=from_date
        )


    if to_date:
        expenses = expenses.filter(
            created_at__date__lte=to_date
        )


    # Calculate total expense
    total = expenses.aggregate(
        Sum("amount")
    )["amount__sum"] or 0



    # Create PDF response
    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Expense_Report.pdf"'
    )


    doc = SimpleDocTemplate(response)



    # PDF table heading
    data = [
        [
            "Amount",
            "Reason",
            "Date & Time"
        ]
    ]



    # Add expense data
    for item in expenses:

        # Convert UTC time to Indian Standard Time
        indian_time = timezone.localtime(
            item.created_at
        )

        data.append(
            [
                f"₹{item.amount}",
                item.reason,
                indian_time.strftime(
                    "%d-%m-%Y %I:%M %p"
                )
            ]
        )



    # Add total row
    data.append(
        [
            "",
            "Total Expense",
            f"₹{total}"
        ]
    )



    # Create table
    table = Table(data)



    # Table styling
    table.setStyle(
        TableStyle([

            # Header
            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.darkblue
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),


            # Border
            (
                "GRID",
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),


            # Expense rows
            (
                "BACKGROUND",
                (0,1),
                (-1,-2),
                colors.beige
            ),


            # Total row
            (
                "BACKGROUND",
                (0,-1),
                (-1,-1),
                colors.lightgrey
            ),


            (
                "FONTNAME",
                (0,-1),
                (-1,-1),
                "Helvetica-Bold"
            ),


            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "CENTER"
            ),

        ])
    )



    # Build PDF
    doc.build(
        [table]
    )


    return response
def download_earnings_pdf(request):

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    earnings = Earnings.objects.all().order_by("-created_at")

    if from_date:
        earnings = earnings.filter(created_at__date__gte=from_date)

    if to_date:
        earnings = earnings.filter(created_at__date__lte=to_date)

    total = earnings.aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Earnings_Report.pdf"'

    doc = SimpleDocTemplate(response)

    data = [["Amount", "Reason", "Date & Time"]]

    for item in earnings:

        data.append([
            f"₹{item.amount}",
            item.reason,
            item.created_at.strftime("%d-%m-%Y %I:%M %p")
        ])

    data.append(["", "", ""])
    data.append(["", "Total Earnings", f"₹{total}"])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.green),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-2), colors.beige),

        ("BACKGROUND", (0,-1), (-1,-1), colors.lightgreen),

        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

    ]))

    doc.build([table])

    return response


# ==========================
# Clear All Data
# ==========================

@login_required(login_url="login")
@require_POST
def clear_all_data(request):

    Expense.objects.filter(
        user=request.user
    ).delete()


    Earnings.objects.filter(
        user=request.user
    ).delete()


    Note.objects.filter(
        user=request.user
    ).delete()



    budget = Budget.objects.filter(
        user=request.user
    ).first()


    if budget:

        budget.fixed_amount = 0
        budget.save()



    return redirect("home")

def findex(request):
    return render(request, "findex.html")
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Registration Successful. Please Login.")
        return redirect("login")

    return render(request, "register.html")


def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)


            # Admin user redirect
            if user.username == "Parathown":
                return redirect("adminpage")


            # Normal users
            return redirect("home")


        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")


    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("findex")


@login_required(login_url="login")
def Home(request):

    storage = None

    db_engine = connection.vendor


    if db_engine == "postgresql":

        # Render PostgreSQL storage

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT pg_size_pretty(
                    pg_database_size(current_database())
                );
                """
            )

            storage = cursor.fetchone()[0]


    elif db_engine == "sqlite":

        # Local SQLite storage

        import os

        db_path = connection.settings_dict["NAME"]

        size_bytes = os.path.getsize(db_path)

        size_mb = round(
            size_bytes / (1024 * 1024),
            2
        )

        storage = f"{size_mb} MB"



    return render(
        request,
        "index.html",
        {
            "storage": storage
        }
    )
@login_required(login_url="login")
def adminpage(request):

    # Only Parathown can access admin page
    if request.user.username != "Parathown":
        return redirect("home")


    search = request.GET.get("search", "")


    users = User.objects.exclude(
        username="Parathown"
    ).order_by("username")


    if search:

        users = users.filter(
            username__icontains=search
        )


    user_data = []


    for user in users:


        user_data.append({

            "user": user,


            "expenses": Expense.objects.filter(
                user=user
            ).order_by("-created_at"),


            "earnings": Earnings.objects.filter(
                user=user
            ).order_by("-created_at"),


            "notes": Note.objects.filter(
                user=user
            ).order_by("-created_at"),


        })


    return render(

        request,

        "adminpage.html",

        {
            "user_data": user_data,
            "search": search
        }

    )
@login_required(login_url="login")
def admin_delete_expense(request, expense_id):

    # Only allow your admin account
    if request.user.username != "Parathown":
        return redirect("home")

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    expense.delete()

    messages.success(
        request,
        "Expense deleted successfully."
    )

    return redirect("adminpage")
@login_required(login_url="login")
def admin_add_expense(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )


    if request.method == "POST":

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")


        budget, created = Budget.objects.get_or_create(

            user=selected_user,

            defaults={
                "fixed_amount":0
            }

        )


        Expense.objects.create(

            user=selected_user,

            budget=budget,

            amount=amount,

            reason=reason

        )


        return redirect("adminpage")



    return render(

        request,

        "admin_add_expense.html",

        {
            "selected_user":selected_user
        }

    )
@login_required(login_url="login")
def admin_update_expense(request, expense_id):

    expense = get_object_or_404(

        Expense,

        id=expense_id

    )


    if request.method == "POST":


        expense.amount = request.POST.get("amount")

        expense.reason = request.POST.get("reason")

        expense.save()


        return redirect("adminpage")



    return render(

        request,

        "admin_update_expense.html",

        {
            "expense":expense
        }

    )

@login_required(login_url="login")
def admin_add_earning(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )


    if request.method == "POST":

        amount = request.POST.get("amount")

        reason = request.POST.get("reason")


        Earnings.objects.create(

            user=selected_user,

            amount=amount,

            reason=reason

        )


        return redirect("adminpage")



    return render(

        request,

        "admin_add_earning.html",

        {
            "selected_user":selected_user
        }

    )
@login_required(login_url="login")
def admin_update_earning(request, earning_id):

    earning = get_object_or_404(

        Earnings,

        id=earning_id

    )


    if request.method == "POST":


        earning.amount = request.POST.get("amount")

        earning.reason = request.POST.get("reason")


        earning.save()


        return redirect("adminpage")



    return render(

        request,

        "admin_update_earning.html",

        {
            "earning":earning
        }

    )
@login_required(login_url="login")
def admin_delete_earning(request, earning_id):

    earning = get_object_or_404(

        Earnings,

        id=earning_id

    )


    earning.delete()


    return redirect("adminpage")
@login_required(login_url="login")
def admin_add_note(request, user_id):

    selected_user = get_object_or_404(
        User,
        id=user_id
    )


    if request.method == "POST":

        content = request.POST.get("content")


        Note.objects.create(

            user=selected_user,

            content=content

        )


        return redirect("adminpage")



    return render(

        request,

        "admin_add_note.html",

        {
            "selected_user": selected_user
        }

    )
@login_required(login_url="login")
def admin_update_note(request, note_id):

    note = get_object_or_404(

        Note,

        id=note_id

    )


    if request.method == "POST":


        note.content = request.POST.get("content")


        note.save()


        return redirect("adminpage")



    return render(

        request,

        "admin_update_note.html",

        {
            "note": note
        }

    )
@login_required(login_url="login")
def admin_delete_note(request, note_id):

    note = get_object_or_404(

        Note,

        id=note_id

    )


    note.delete()


    return redirect("adminpage")