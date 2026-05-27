from django.conf import settings
from django.db import models


class ContactRequest(models.Model):
    bid = models.ForeignKey(
        'bids.Bid',
        on_delete=models.CASCADE,
        related_name='contact_requests',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_contact_requests',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_contact_requests',
    )
    comment = models.TextField(blank=True)
    sender_phone_snapshot = models.CharField(max_length=20)
    sender_organization_snapshot = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bid', 'sender'],
                name='unique_contact_request_per_bid_sender',
            )
        ]
        indexes = [
            models.Index(fields=['receiver', 'is_read', '-created_at']),
            models.Index(fields=['sender', '-created_at']),
            models.Index(fields=['bid']),
        ]

    def __str__(self):
        return f'ContactRequest #{self.pk}: {self.sender} -> {self.receiver} (bid #{self.bid_id})'
