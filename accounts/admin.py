from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'Profile',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'phone_number',
                    'otp',
                    'otp_valid_till',
                ),
            },
        ),
        (  # new fieldset added on to the bottom
            'Meta Data',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'created_on',
                    'updated_on',
                    'is_deleted',
                    'tenant_schema_name',
                    'tenant_created_by_user_id',
                    'tenant_updated_by_user_id',
                ),
            },
        ),
    )

    readonly_fields = ('created_on', 'updated_on',)


admin.site.register(User, CustomUserAdmin)
