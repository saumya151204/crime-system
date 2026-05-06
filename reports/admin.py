from django.contrib import admin
from .models import CrimeReport

class CrimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'location')

admin.site.register(CrimeReport)