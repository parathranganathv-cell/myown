from django.db import models
from django.contrib.auth.models import User


# ===========================
# Budget
# ===========================

class Budget(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    fixed_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "budget_table"


    def __str__(self):
        return str(self.fixed_amount)



# ===========================
# Expense
# ===========================

class Expense(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reason = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "expense_table"
        ordering = ["-created_at"]


    def __str__(self):
        return str(self.amount)



# ===========================
# Earnings
# ===========================

class Earnings(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reason = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "earning_table"
        ordering = ["-created_at"]


    def __str__(self):
        return str(self.amount)



# ===========================
# Notes
# ===========================

class Note(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        db_table = "note_table"


    def __str__(self):
        return self.content

# ===========================
# Calendar Events
# ===========================

class CalendarEvent(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        db_table = "calendar_event_table"


    def __str__(self):

        return self.title