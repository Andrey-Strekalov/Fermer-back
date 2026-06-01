from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_CONTACT_REQUEST_CREATED = 'contact_request_created'

    TYPE_CHOICES = [
        (TYPE_CONTACT_REQUEST_CREATED, 'Новый контактный запрос'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    contact_request = models.ForeignKey(
        'contacts.ContactRequest',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    payload = models.JSONField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['recipient', 'is_read', '-created_at'])]
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification #{self.pk}: {self.type} → {self.recipient}'
