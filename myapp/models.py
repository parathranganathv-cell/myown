from django.db import models


# ===========================
# Budget
# ===========================
class Budget(models.Model):

    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "budget_table"

    def __str__(self):
        return str(self.fixed_amount)


# ===========================
# Expense
# ===========================
class Expense(models.Model):

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    reason = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "expense_table"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.amount)


# ===========================
# Earnings
# ===========================
class Earnings(models.Model):

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    reason = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "earning_table"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.amount)


# ===========================
# Notes
# ===========================
class Note(models.Model):

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content