from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.views.decorators.http import require_POST

from .models import Budget, Expense, Earnings, Note


# ======================
# Home
# ======================

def Home(request):
    return render(request, "index.html")


# ======================
# Expense Page
# ======================

# ======================
# Expense Page
# ======================

# ======================
# Expense Page
# ======================

def Amount(request):

    # -------------------------
    # Clear Budget
    # -------------------------
    if request.method == "POST" and "clear_budget" in request.POST:

        budget = Budget.objects.first()

        if budget:
            budget.fixed_amount = 0
            budget.save()

        return redirect("amount")

    # -------------------------
    # Save Budget
    # -------------------------
    if request.method == "POST" and "save_budget" in request.POST:

        fixed_amount = request.POST.get("fixed_amount")

        budget = Budget.objects.first()

        if budget:
            budget.fixed_amount = fixed_amount
            budget.save()
        else:
            budget = Budget.objects.create(
                fixed_amount=fixed_amount
            )

        return redirect("amount")

    # -------------------------
    # Save Expense
    # -------------------------
    if request.method == "POST" and "save_expense" in request.POST:

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")

        budget = Budget.objects.first()

        # Automatically create a budget if none exists
        if budget is None:
            budget = Budget.objects.create(fixed_amount=0)

        Expense.objects.create(
            budget=budget,
            amount=amount,
            reason=reason
        )

        return redirect("amount")

    # -------------------------
    # Display Data
    # -------------------------

    budget = Budget.objects.first()

    if budget:

        amounts = Expense.objects.filter(
            budget=budget
        ).order_by("-created_at")

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

    }

    return render(request, "amount.html", context)

def Earning(request):

    if request.method == "POST":

        amount = request.POST.get("amount")
        reason = request.POST.get("reason")

        Earnings.objects.create(
            amount=amount,
            reason=reason
        )

        return redirect("earning")


    # -------------------------
    # Filter
    # -------------------------

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    amounts = Earnings.objects.all().order_by("-created_at")

    if from_date:
        amounts = amounts.filter(created_at__date__gte=from_date)

    if to_date:
        amounts = amounts.filter(created_at__date__lte=to_date)


    total_amount = amounts.aggregate(
        Sum("amount")
    )["amount__sum"] or 0


    context = {

        "amounts": amounts,

        "total_amount": total_amount,

        "from_date": from_date,

        "to_date": to_date,

    }

    return render(request, "myearnings.html", context)
# ======================
# Notes
# ======================

def mynotes(request):

    if request.method == "POST":

        content = request.POST.get("content")

        if content:

            Note.objects.create(content=content)

        return redirect("note")

    notes = Note.objects.all().order_by("-created_at")

    return render(request, "mynotes.html", {"notes": notes})


# ======================
# Calendar
# ======================

def Calender(request):
    return render(request, "calender.html")


# ======================
# PDF
# ======================

def download_pdf(request):

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = 'attachment; filename="Earnings.pdf"'

    doc = SimpleDocTemplate(response)

    data = [["Amount", "Reason", "Date"]]

    for item in Earnings.objects.all():

        data.append([
            str(item.amount),
            item.reason,
            item.created_at.strftime("%d-%m-%Y %I:%M %p")
        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

    ]))

    doc.build([table])

    return response



from django.views.decorators.http import require_POST

@require_POST
def clear_all_data(request):

    Expense.objects.all().delete()
    Earnings.objects.all().delete()
    Note.objects.all().delete()

    # Don't delete the Budget row.
    budget = Budget.objects.first()

    if budget:
        budget.fixed_amount = 0
        budget.save()
    else:
        Budget.objects.create(fixed_amount=0)

    return redirect("home")