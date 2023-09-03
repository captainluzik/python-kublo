from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'is_staff', 'is_active', 'date_joined', ]
    list_filter = ['is_staff', 'is_active', ]
    ordering = ['email', ]
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

