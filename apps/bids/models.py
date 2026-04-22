from django.conf import settings
from django.db import models


class Bid(models.Model):
    TYPE_BUY = 'buy'
    TYPE_SELL = 'sell'
    TYPE_CHOICES = (
        (TYPE_BUY, 'Buy'),
        (TYPE_SELL, 'Sell'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
    )

    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    quality = models.CharField(max_length=255, blank=True, default='')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.DecimalField(max_digits=12, decimal_places=3)
    region = models.CharField(max_length=255)
    comment = models.TextField(blank=True, default='')

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-published_at', '-id')

    def __str__(self) -> str:
        return f'Bid#{self.pk} {self.type} {self.title}'

