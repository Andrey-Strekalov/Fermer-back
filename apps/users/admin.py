from django.contrib import admin

from .models import User, PhoneOTP, Requisites

class UserAdmin(admin.ModelAdmin):
    # Используем get_username вместо username
    list_display = ['get_username', 'phone_number', 'role', 'is_staff']
    list_display_links = ['get_username']  # клик по составному имени ведёт к редактированию

    def get_username(self, obj):
        """Возвращает составное имя или номер телефона"""
        return obj.first_name if obj.first_name else obj.phone_number

    get_username.short_description = 'USERNAME'

    # Поиск по номеру телефона и имени
    search_fields = ['phone_number', 'first_name', 'last_name']

    # Сортировка по умолчанию
    ordering = ['-date_joined']

    # Переопределяем fieldsets: убираем username
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Переопределяем add_fieldsets для создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'role'),
        }),
    )


class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'is_used')
    search_fields = ('phone_number',)
    list_display_links = ('phone_number',)

@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'inn', 'bik')
    search_fields = ('company_name', 'inn', 'user__phone_number')


admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)

