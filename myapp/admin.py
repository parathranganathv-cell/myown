from django.contrib import admin

# Register your models here.
from .models import Expense, Earnings, Note

admin.site.register(Expense)
admin.site.register(Earnings)
admin.site.register(Note)