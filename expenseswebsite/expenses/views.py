from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
# import xlwt
from openpyxl import Workbook

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

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

def stats_view(request):
    return render(request, 'expenses/stats.html')

def expense_category_summary(request):
    today_date = datetime.date.today()
    six_months_ago = today_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(date__gte=six_months_ago, date__lte=today_date, owner=request.user)

    final_rep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(categoryToSearch):    
        amount = 0
        ''' -To return the expenses belonging to the passed category - '''
        filtered_by_category = expenses.filter(category=categoryToSearch)

        ''' -To increment (add on to) the initial zero amount with the sum totals for that category- '''
        for item in filtered_by_category:
            amount+=item.amount

        return amount
        
    for x in expenses:
        for y in category_list:
            final_rep[y]=get_expense_category_amount(y)

    return JsonResponse({
        'expense_category_data': final_rep
    }, safe=False)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    # writing header
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    # writing subsequent rows
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response

def export_excel(request): 
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'

    # wb = xlwt.Workbook(encoding='utf-8')
    # ws = wb.add_sheet('Expenses')

    # # writing header
    # row_num = 0
    # font_style = xlwt.XFStyle() # defaultlt
    # font_style.font.bold = True # making font bold
    # columns = ['Amount', 'Description', 'Category', 'Date']

    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style)

    # # writing subsequent rows
    # font_style = xlwt.XFStyle()
    # rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')

    # for row in rows:
    #     row_num += 1

    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, str(row[col_num]), font_style)

    # wb.save(response)
    # return response
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xlsx'

    wb = Workbook()
    ws = wb.active
    ws.title = 'Expenses'

    # Writing header
    columns = ['Amount', 'Description', 'Category', 'Date']
    ws.append(columns)

    # Writing data rows
    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    for row in rows:
        ws.append(row)

    wb.save(response)
    return response

def export_pdf(request):
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition']='inline; attachment; filename=Expenses'+str(datetime.datetime.now())+'.pdf'
    # response['Content-Transfer-Encoding']='binary'

    # html_string = render_to_string('expenses/pdf-output.html', {'expenses': [], 'total': 0})

    # html = HTML(string=html_string)

    # result = html.write_pdf()

    # # to preview file in memory (read file in temporary mode) before you can e.g. print / download
    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()

    #     output = open(output.name, 'rb')
    #     response.write(output.read())
    
    # return response

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; attachment; filename="Expenses_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner=request.user)
    expensesSum = expenses.aggregate(Sum('amount'))

    # Render HTML template to string
    # html_string = render_to_string('expenses/pdf-output.html', {'expenses': [], 'total': 0})
    html_string = render_to_string('expenses/pdf-output.html', {'expenses':expenses, 'total': expensesSum['amount__sum']})
    html = HTML(string=html_string)

    # Generate PDF in memory
    pdf_content = html.write_pdf()

    # Write the PDF content to the response
    response.write(pdf_content)

    return response
