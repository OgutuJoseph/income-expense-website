from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expensesUrl'),
    path('add-expense', views.add_expense, name='addExpensesUrl'),
    path('edit-expense/<int:id>', views.edit_expense, name='editExpensesUrl'),
    path('delete-expense/<int:id>', views.delete_expense, name='deleteExpensesUrl'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='searchExpensesUrl')
]