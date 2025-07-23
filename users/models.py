from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import TimestampedModel

class User(AbstractUser):
    class UserType(models.TextChoices):
        BUYER = 'BUYER', 'Buyer'
        FARMER = 'FARMER', 'Farmer'
        ADMIN = 'ADMIN', 'Admin'

    email = models.EmailField(unique=True, help_text="Required. Used for login.")
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.BUYER)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="e.g., 0712345678")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()