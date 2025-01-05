from django.contrib import admin
from .models import FederatedLearningResult
from unfold.admin import ModelAdmin


  
# Register your models here.

class FederatedLearningResultAdmin(ModelAdmin):
  list_display = ('id',"processed_time","data")  # Fields to display in the admin list view
  list_filter = ('processed_time','data')  # Filter data by status
  search_fields = ('data_description',)  # Allow searching by description


admin.site.register(FederatedLearningResult, FederatedLearningResultAdmin)


