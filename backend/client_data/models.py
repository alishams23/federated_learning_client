from django.db import models

# Create your models here.

class ClientData(models.Model):
    description = models.TextField(verbose_name="توضیحات")
    uploaded_file = models.FileField(upload_to='client_data/',verbose_name="فایل")  # Path to the uploaded file
    upload_time = models.DateTimeField(auto_now_add=True,verbose_name="زمان آپدیت")  # Timestamp for upload
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('processed', 'Processed')], default='pending',verbose_name="وضعیت")  # Data processing status

    class Meta:
        verbose_name = "داده"
        verbose_name_plural = "داده ها "

    # def __str__(self):
    #     return self.client_id