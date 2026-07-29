from django.contrib import admin

# Register your models here.
from .models import Budget, Expense, Earnings, Note


admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Earnings)
admin.site.register(Note)