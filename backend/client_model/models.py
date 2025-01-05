from django.db import models

from client_data.models import ClientData

# Create your models here.

class FederatedLearningResult(models.Model):
    data = models.ForeignKey(ClientData, on_delete=models.CASCADE, related_name='results',verbose_name="داده")  # Link to ClientData
    metrics = models.JSONField(verbose_name="متریک ها")  # JSON field to store metrics (e.g., accuracy, loss)
    model_path = models.FileField(upload_to='models/', null=True, blank=True,verbose_name="فایل مدل آموزش دیده شده")  # Path to the trained model
    processed_time = models.DateTimeField(auto_now_add=True,verbose_name="زمان پردازش شده")  # Timestamp for completion
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخنه شده")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")

    class Meta:
        verbose_name = "مدل"
        verbose_name_plural = "مدل ها"

    def __str__(self):
        return f"Results for {self.data.id}"