from django.db import models

from client_data.models import ClientData

# Create your models here.

class FederatedLearningResult(models.Model):
    data = models.ForeignKey(ClientData, on_delete=models.CASCADE, related_name='results')  # Link to ClientData
    metrics = models.JSONField()  # JSON field to store metrics (e.g., accuracy, loss)
    model_path = models.FileField(upload_to='models/', null=True, blank=True)  # Path to the trained model
    processed_time = models.DateTimeField(auto_now_add=True)  # Timestamp for completion

    def __str__(self):
        return f"Results for {self.data.id}"