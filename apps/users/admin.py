from django.contrib import admin

from .models import User, PhoneOTP

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'phone_number']


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'is_used')
    search_fields = ('phone_number',)
    list_display_links = ('phone_number',)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)

