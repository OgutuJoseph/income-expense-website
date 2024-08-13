from django.contrib import admin
from .models import Expense, Category

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'description', 'date', 'owner',)
    search_fields = ('category', 'amount', 'description', 'date', 'owner',)

    list_per_page = 3

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)