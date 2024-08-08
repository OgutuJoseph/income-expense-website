from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expensesUrl'),
    path('add-expense', views.add_expense, name='addExpensesUrl')
]