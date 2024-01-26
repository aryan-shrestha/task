from django.contrib import admin
from .models import Company, CompanyDetail

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'LTP', 'pt_change', 'percentage_change', 'added')
    
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyDetail)