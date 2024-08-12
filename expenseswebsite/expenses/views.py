from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator

# Expenses views.

@login_required(login_url='authentication/login')
def index(request):
    categories = Category.objects.all()
    userExpenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(userExpenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'userExpenses': userExpenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)

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
        descriptionInput  = request.POST['description']
        categoryInput  = request.POST['category']
        dateInput  = request.POST['expense_date']

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
            owner  = request.user
        )
        messages.success(request, 'Expense added successfully.')
        return redirect('expensesUrl')

@login_required(login_url='authentication/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
            'expense': expense,
            'values': expense,
            'categorySet' : categories,
        }
    
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)        
    if request.method == 'POST':
        amountInput = request.POST['amount']
        descriptionInput  = request.POST['description']
        categoryInput  = request.POST['category']
        dateInput  = request.POST['expense_date']

        if not amountInput:
            messages.error(request, 'Amount field is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not descriptionInput:
            messages.error(request, 'Description field is required')
            return render(request, 'expenses/edit_expense.html', context)

        expense.amount = amountInput
        expense.description = descriptionInput
        expense.category = categoryInput
        expense.date = dateInput
        expense.owner  = request.user
        expense.save()
        messages.success(request, 'Expense updated successfully.')
        return redirect('expensesUrl')

@login_required(login_url='authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('expensesUrl')