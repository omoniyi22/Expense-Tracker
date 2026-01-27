from django.urls import path
from . import views

urlpatterns = [
    # Budget URLs
    path('', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/create/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budget/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budget/<int:pk>/update/', views.BudgetUpdateView.as_view(), name='budget_update'),
    path('budget/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget_delete'),
    
    # Expense URLs
    path('budget/<int:budget_id>/expense/create/', views.create_expense, name='expense_create'),
    path('expense/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
]