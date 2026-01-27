from django.db import models
from django.urls import reverse

class Budget(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('budget_detail', kwargs={'pk': self.pk})

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())

    def remaining_amount(self):
        return self.amount - self.total_expenses()

    def is_over_budget(self):
        return self.remaining_amount() < 0

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ${self.amount}"

    class Meta:
        ordering = ['-created_at']