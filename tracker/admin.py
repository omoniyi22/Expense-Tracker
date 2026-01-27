from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Budget, Expense

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'total_expenses', 'remaining_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'note']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'budget', 'created_at']
    list_filter = ['created_at', 'budget']
    search_fields = ['title']