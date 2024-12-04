from django.contrib import admin

from .models import ClientData
# Register your models here.

class ClientDataAdmin(admin.ModelAdmin):
    list_display = ('description', 'uploaded_file', 'upload_time', 'status')  # Fields to display in the admin list view
    list_filter = ('status',)  # Filter data by status
    search_fields = ('description',)  # Allow searching by description
    ordering = ('-upload_time',)  # Default ordering by upload time in descending order

admin.site.register(ClientData, ClientDataAdmin)