from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.html import format_html


# Create your models here.





class User(AbstractUser):
    token_server = models.TextField(blank=True,null=True)
    

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    