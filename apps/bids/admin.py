from django.contrib import admin

from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title', 'price', 'volume', 'region', 'is_archived', 'published_at', 'author')
    list_filter = ('type', 'region', 'is_archived')
    search_fields = ('title', 'quality', 'region', 'comment', 'author__phone_number', 'author__first_name')

