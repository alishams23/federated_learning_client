from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ClientData
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.

class ClientDataAdmin(ModelAdmin):
    list_display = ('description',"id", 'is_processed',  'status','redirect_button',)  # Fields to display in the admin list view
    list_filter = ('status','upload_time')  # Filter data by status
    search_fields = ('description',)  # Allow searching by description
    ordering = ('-upload_time',)  # Default ordering by upload time in descending order
    
    def save_model(self, request, obj, form, change):
        # Automatically set the author to the logged-in user on creation
        if not obj.pk:  # If the object is being created
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Limit queryset to only show objects created by the logged-in user
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        # Allow change permission only if the author matches the logged-in user
        if obj and obj.author != request.user:
            return False
        return super().has_change_permission(request, obj=obj)
    
    def redirect_button(self, obj):
        # Generate a URL to the specific page
        url = reverse('client_data:generating_model', kwargs={'id': obj.id})
        if obj.is_processed() == False : return  format_html('<a class=" rounded-md bg-primary-600 text-white py-1 flex justify-center" href="{}">شروع   <span class="material-symbols-outlined  pl-2" >play_arrow</span> </a>', url)
        else : return format_html('')
        
    
    redirect_button.short_description = "شروع آموزش"
    redirect_button.allow_tags = True  # This line is optional in modern Django
    

admin.site.register(ClientData, ClientDataAdmin)