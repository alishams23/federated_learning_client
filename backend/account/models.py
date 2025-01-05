from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator

# Create your models here.





class User(AbstractUser):
    token_server = models.TextField(blank=True,null=True)
    

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    
    

class Server(models.Model):
    ip = models.CharField(
        max_length=60,  
       verbose_name='ایپی همراه با پورت یا دامنه ',
       help_text=" example:  http:// 0.0.0.0:8000"
    )
    username = models.TextField(verbose_name="یوزرنیم")
    password = models.TextField(verbose_name="رمز عبور")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخنه شده")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")

    class Meta:
        verbose_name = "سرور"
        verbose_name_plural = "سرور ها "

    def __str__(self):
        return f"{self.ip} -- {self.id}"
    
    
    
    

class Error(models.Model):
    error = models.TextField(verbose_name="ارور")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان ساخنه شده")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="زمان بروز رسانی")


    class Meta:
        verbose_name = "ارور"
        verbose_name_plural = "ارور ها "

    def __str__(self):
        return f"{self.ip} -- {self.id}"
    
