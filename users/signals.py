from .models import NewUser, PhoneOTP
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=NewUser)
def post_save_generate_otpe(sender, instance, created, *args, **kwargs):
    if created:
        PhoneOTP.objects.create(user=instance)
        
        
