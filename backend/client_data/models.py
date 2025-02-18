from django.db import models
from account.models import User, Server
# Create your models here.


class ClientData(models.Model):
    description = models.TextField(verbose_name="توضیحات")
    uploaded_file = models.FileField(
        upload_to='client_data/', verbose_name="فایل")  # Path to the uploaded file
    upload_time = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان آپدیت")  # Timestamp for upload
    status = models.CharField(max_length=50, choices=[('not_started', 'شروع نشده'), ('pending', 'در حال پردازش'), (
        'processed', 'پردازش شده')], default='not_started', verbose_name="وضعیت")  # Data processing status
    server = models.ForeignKey(
        Server, verbose_name="سرور", on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, verbose_name="نویسنده", on_delete=models.CASCADE)
    repeat_count = models.IntegerField(default=1, verbose_name="تعداد تکرار")
    time_repeated = models.IntegerField(
        verbose_name="زمان تکرار به دقیقه")
    repeated_count = models.IntegerField(verbose_name="تعداد دفعات تکرار شده " , default=0)

    class Meta:
        verbose_name = "داده"
        verbose_name_plural = "داده ها "

    def __str__(self):
        return f"{self.description} -- {self.id}"

    def is_processed(self):
        return self.status == "processed"

    is_processed.boolean = True
    is_processed.short_description = 'پردازش شده'

    # def __str__(self):
    #     return self.client_id
