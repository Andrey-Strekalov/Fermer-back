from django.contrib import admin

from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sender', 'receiver', 'bid', 'is_read',
        'sender_phone_snapshot', 'sender_organization_snapshot', 'created_at',
    )
    list_filter = ('is_read', 'created_at')
    search_fields = (
        'sender__phone_number', 'sender__first_name',
        'receiver__phone_number', 'receiver__first_name',
        'sender_phone_snapshot', 'sender_organization_snapshot',
        'comment',
    )
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('bid', 'sender', 'receiver')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
