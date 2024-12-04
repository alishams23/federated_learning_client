from django.db import models

# Create your models here.

class ClientData(models.Model):
    description = models.TextField()
    uploaded_file = models.FileField(upload_to='client_data/')  # Path to the uploaded file
    upload_time = models.DateTimeField(auto_now_add=True)  # Timestamp for upload
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('processed', 'Processed')], default='pending')  # Data processing status

    # def __str__(self):
    #     return self.client_id