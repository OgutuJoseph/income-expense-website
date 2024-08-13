from django.contrib import admin
from .models import Income, Source

# Register your models here.

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'description', 'date', 'owner',)
    search_fields = ('source', 'amount', 'description', 'date', 'owner',)
    
    list_per_page = 3

admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)