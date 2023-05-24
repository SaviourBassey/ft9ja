from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserBalance


@receiver(post_save, sender=User)
def create_userbalance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_userbalance(sender, instance, **kwargs):
    instance.userbalance.save()