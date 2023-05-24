from django.db import models
from django.contrib.auth.models import User

# Create your models here.
RESULT = (  ("profit","profit"),
            ("loss","loss"),
          )

class UserTrades(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=10, choices=RESULT)
    trade_type = models.CharField(max_length=10, blank=True, null=True)
    trade_amount = models.IntegerField()
    new_bal = models.FloatField(blank=True, null=True)
    entry_point = models.FloatField(blank=True, null=True)
    exit_point = models.FloatField(blank=True, null=True)
    currency_pair = models.CharField(max_length=10, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def formatted_timestamp(self):
        return self.timestamp.strftime("%H:%M")