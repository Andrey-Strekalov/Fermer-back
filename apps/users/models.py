from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )

    username = None
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='farmer'
    )
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name if self.first_name else self.phone_number


@receiver(post_save, sender=User)
def set_user_first_name(sender, instance, created, **kwargs):
    """
    После создания пользователя формируем first_name = user_<id>.
    """
    if created and not instance.first_name:  # только при создании и если first_name пусто
        instance.first_name = f"user_{instance.id}"
        # Сохраняем, избегая повторного вызова сигнала
        instance.save(update_fields=['first_name'])



class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.phone_number} ({self.code})'
