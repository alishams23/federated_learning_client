from django.contrib import admin
from .models import FederatedLearningResult
from unfold.admin import ModelAdmin


  
# Register your models here.

class FederatedLearningResultAdmin(ModelAdmin):
  
  pass

admin.site.register(FederatedLearningResult, FederatedLearningResultAdmin)


