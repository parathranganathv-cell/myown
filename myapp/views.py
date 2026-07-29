from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.utils import timezone

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from .models import Budget, Expense, Earnings, Note


# ==========================
# Home
# ==========================

def Home(request):
    return render(request, "index.html")


# ==========================
# Expense Page
# ==========================

def Amount(request):

    # --------------------
    # Clear Budget
    # --------------------

    if request.method == "POST" and "clear_budget" in request.POST:

        budget = Budget.objects.first()

        if budget:
            budget.fixed_amount = 0
            budget.save()

        return redirect("amount")

    # --------------------
    # Save Budget
    # --------------------

    if request.method == "POST" and "save_budget" in request.POST:

        fixed_amount = request.POST.get("fixed_amount")

        budget = Budget.objects.first()

        if budget:

            budget.fixed_amount = fixed_amount
            budget.save()

        else:

            Budget.objects.create(
                fixed_amount=fixed_amount
            )

        return redirect("amount")

    # --------------------
    # Save Expense
    # --------------------

    if request.method == "POST" and "save_expense" in request.POST:

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")

        budget = Budget.objects.first()

        if budget is None:

            budget = Budget.objects.create(
                fixed_amount=0
            )

        Expense.objects.create(
            budget=budget,
            amount=amount,
            reason=reason
        )

        return redirect("amount")

    # --------------------
    # Filter
    # --------------------

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    budget = Budget.objects.first()

    if budget:

        amounts = Expense.objects.filter(
            budget=budget
        ).order_by("-created_at")

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

    else:

        amounts = Expense.objects.none()

        fixed_amount = 0

        total_amount = 0

        remaining_amount = 0

    context = {

        "amounts": amounts,

        "fixed_amount": fixed_amount,

        "remaining_amount": remaining_amount,

        "total_amount": total_amount,

        "from_date": from_date,

        "to_date": to_date,

    }

    return render(
        request,
        "amount.html",
        context
    )
# ==========================
# Earnings Page
# ==========================

def Earning(request):

    # --------------------
    # Save Earnings
    # --------------------

    if request.method == "POST":

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")

        Earnings.objects.create(
            amount=amount,
            reason=reason
        )

        return redirect("earning")

    # --------------------
    # Filter
    # --------------------

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    amounts = Earnings.objects.all().order_by("-created_at")

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

    context = {

        "amounts": amounts,

        "total_amount": total_amount,

        "from_date": from_date,

        "to_date": to_date,

    }

    return render(
        request,
        "myearnings.html",
        context
    )


# ==========================
# Notes
# ==========================

def mynotes(request):

    if request.method == "POST":

        content = request.POST.get("content")

        if content:
            Note.objects.create(
                content=content
            )

        return redirect("note")

    notes = Note.objects.all().order_by("-created_at")

    return render(
        request,
        "mynotes.html",
        {
            "notes": notes
        }
    )

# ==========================
# Calendar
# ==========================

def Calender(request):

    return render(
        request,
        "calender.html"
    )
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

@require_POST
def clear_all_data(request):

    Expense.objects.all().delete()
    Earnings.objects.all().delete()
    Note.objects.all().delete()

    budget = Budget.objects.first()

    if budget:

        budget.fixed_amount = 0
        budget.save()

    else:

        Budget.objects.create(
            fixed_amount=0
        )

    return redirect("home")