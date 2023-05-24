from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.FloatField(default=100.00)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #Create this model automatically when user object is created

    class Meta:
        verbose_name = ("User Balance")
        verbose_name_plural = ("User Balance")
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.user.username} Accounts Balance"
