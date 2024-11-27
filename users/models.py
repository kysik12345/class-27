
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):
#     phone = models.CharField(max_length=50, verbose_name="Телефон")
#     city = models.CharField(max_length=50, verbose_name="Город")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
    birth_data = models.DateField(null=True, blank=True)
    


