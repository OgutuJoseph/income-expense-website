from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime

# Expenses views.

@login_required(login_url='authentication/login')
def index(request):
    categories = Category.objects.all()
    userExpenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(userExpenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    # currency = UserPreference.objects.get(user=request.user).currency 

    # try:
    #     currency = UserPreference.objects.get(user=request.user).currency
    # except UserPreference.DoesNotExist:
    #     currency = '[[ X Currency ]]'

    user_preference, created = UserPreference.objects.get_or_create(
        user=request.user,
        defaults={'currency': '[[ X Currency ]]'}
    )
    currency = user_preference.currency

    context = {
        'userExpenses': userExpenses,
        'page_obj': page_obj,
        'currency': currency
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

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        
        data = expenses.values()

        return JsonResponse(list(data), safe=False)

def expense_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(date__gte=six_months_ago, date__lte=today_date)

    final_rep = {}

    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))