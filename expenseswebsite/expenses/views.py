from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Expenses views.

@login_required(login_url='authentication/login')
def index(request):
    categories = Category.objects.all()
    return render(request, 'expenses/index.html')

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categorySet' : categories,
        'values': request.POST
    }

    if request.method == 'GET':        
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amountInput = request.POST['amount']
        descriptionInput  =request.POST['description']
        categoryInput  =request.POST['category']
        dateInput  =request.POST['expense_date']

        if not amountInput:
            messages.error(request, 'Amount field is required')
            return render(request, 'expenses/add_expense.html', context)
        if not descriptionInput:
            messages.error(request, 'Description field is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            amount = amountInput,
            description = descriptionInput,
            category = categoryInput,
            date = dateInput,
            owner  =request.user
        )
        messages.success(request, 'Expense added successfully.')
        return redirect('expensesUrl')