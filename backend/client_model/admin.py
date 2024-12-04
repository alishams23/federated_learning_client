from django.contrib import admin
from .models import FederatedLearningResult
# Register your models here.

class FederatedLearningResultAdmin(admin.ModelAdmin):
  pass

admin.site.register(FederatedLearningResult, FederatedLearningResultAdmin)
