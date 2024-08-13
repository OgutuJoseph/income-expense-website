from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference

# Incomes views.

@login_required(login_url='authentication/login')
def index(request):
    sources = Source.objects.all()
    userIncomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(userIncomes, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'userIncomes': userIncomes,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sourceSet' : sources,
        'values': request.POST
    }

    if request.method == 'GET':        
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amountInput = request.POST['amount']
        descriptionInput  = request.POST['description']
        sourceInput  = request.POST['source']
        dateInput  = request.POST['income_date']

        if not amountInput:
            messages.error(request, 'Amount field is required')
            return render(request, 'income/add_income.html', context)
        if not descriptionInput:
            messages.error(request, 'Description field is required')
            return render(request, 'income/add_income.html', context)

        Income.objects.create(
            amount = amountInput,
            description = descriptionInput,
            source = sourceInput,
            date = dateInput,
            owner  = request.user
        )
        messages.success(request, 'Income added successfully.')
        return redirect('incomesUrl')

@login_required(login_url='authentication/login')
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
            'income': income,
            'values': income,
            'sourceSet' : sources,
        }
    
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)        
    if request.method == 'POST':
        amountInput = request.POST['amount']
        descriptionInput  = request.POST['description']
        sourceInput  = request.POST['source']
        dateInput  = request.POST['income_date']

        if not amountInput:
            messages.error(request, 'Amount field is required')
            return render(request, 'income/edit_income.html', context)
        if not descriptionInput:
            messages.error(request, 'Description field is required')
            return render(request, 'income/edit_income.html', context)

        income.amount = amountInput
        income.description = descriptionInput
        income.source = sourceInput
        income.date = dateInput
        income.owner  = request.user
        income.save()
        messages.success(request, 'Income updated successfully.')
        return redirect('incomesUrl')

@login_required(login_url='authentication/login')
def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully.')
    return redirect('incomesUrl')

def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        
        data = incomes.values()

        return JsonResponse(list(data), safe=False)