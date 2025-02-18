from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, unique=True)
    token_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.verification_token and self.token_expiry:
            if timezone.now() > self.token_expiry:
                logger.warning(f'Expired token found for user: {self.user.username}')
                raise ValidationError('Token has expired')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def cleanup_expired_tokens():
    """Clean up expired verification tokens"""
    expired_profiles = Profile.objects.filter(
        token_expiry__lt=timezone.now()
    ).exclude(verification_token='')
    
    if expired_profiles.exists():
        count = expired_profiles.update(verification_token='')
        logger.info(f'Cleaned up {count} expired verification tokens')
