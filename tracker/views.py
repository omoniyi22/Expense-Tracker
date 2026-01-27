from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm

# Budget Views
class BudgetListView(ListView):
    model = Budget
    template_name = 'tracker/budget_list.html'
    context_object_name = 'budgets'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budgets = context['budgets']
        
        # Calculate totals
        total_budget_amount = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = sum(budget.total_expenses() for budget in budgets)
        total_remaining = total_budget_amount - total_expenses
        
        context.update({
            'total_budget_amount': total_budget_amount,
            'total_expenses': total_expenses,
            'total_remaining': total_remaining,
        })
        return context



class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'tracker/budget_form.html'
    success_url = reverse_lazy('budget_list')

    def form_valid(self, form):
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)

class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'tracker/budget_detail.html'
    context_object_name = 'budget'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_form'] = ExpenseForm()
        context['expenses'] = self.object.expenses.all()
        return context

class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'tracker/budget_form.html'

    def get_success_url(self):
        return reverse_lazy('budget_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Budget updated successfully!')
        return super().form_valid(form)

class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'tracker/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Budget deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Expense Views
def create_expense(request, budget_id):
    budget = get_object_or_404(Budget, pk=budget_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.budget = budget
            expense.save()
            messages.success(request, 'Expense added successfully!')
    return redirect('budget_detail', pk=budget_id)

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'tracker/expense_form.html'

    def get_success_url(self):
        return reverse_lazy('budget_detail', kwargs={'pk': self.object.budget.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully!')
        return super().form_valid(form)

class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('budget_detail', kwargs={'pk': self.object.budget.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Expense deleted successfully!')
        return super().delete(request, *args, **kwargs)