from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='incomesUrl'),
    path('add-income', views.add_income, name='addIncomesUrl'),
    path('edit-income/<int:id>', views.edit_income, name='editIncomesUrl'),
    path('delete-income/<int:id>', views.delete_income, name='deleteIncomesUrl'),
    path('search-incomes', csrf_exempt(views.search_incomes), name='searchIncomesUrl')
]