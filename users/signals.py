import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

def _generate_code():
    return str(random.randint(100000, 999999))

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        code = _generate_code()
        instance.activation_code = code
        instance.save()
        # Send email to console backend
        send_mail(
            subject='Activation code',
            message=f'Your activation code: {code}',
            from_email='noreply@example.com',
            recipient_list=[instance.email],
        )
