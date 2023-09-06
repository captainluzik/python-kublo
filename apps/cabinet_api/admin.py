from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.cabinet_api.models import CustomUser, PersonalAccount


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'is_staff', 'is_active', 'date_joined', ]
    list_filter = ['is_staff', 'is_active', ]
    ordering = ['email', ]
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


@admin.register(PersonalAccount)
class PersonalAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_partners', 'deposit_term',
                    'total_deposit_amount', 'interest_rate', 'dividend_amount',)
    list_filter = ('investment_sector', 'deposit_term',)
    search_fields = ('partner_code', 'user__email', 'investment_sector',)
    raw_id_fields = ('user', )

    def get_partners(self, obj):
        return ", ".join([partner.email for partner in obj.partners.all()])

    get_partners.short_description = 'Partners'
