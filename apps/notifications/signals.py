from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contacts.models import ContactRequest
from .models import Notification


@receiver(post_save, sender=ContactRequest)
def create_notification_on_contact_request(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        recipient=instance.receiver,
        type=Notification.TYPE_CONTACT_REQUEST_CREATED,
        contact_request=instance,
        payload={
            'bid_title': instance.bid.title,
            'sender_first_name': instance.sender.first_name,
        },
    )
