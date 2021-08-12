from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from services.models import *


class TemplateAdmin(admin.ModelAdmin):
    model = Template
    readonly_fields = ('created_on', 'modified_on')


class DataSheetAdmin(admin.ModelAdmin):
    model = DataSheet


class CertificateAdmin(admin.ModelAdmin):
    model = Certificate


class DataKeyAdmin(admin.ModelAdmin):
    model = DataKey


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    # readonly_fields = ['otp_valid_till']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(DataSheet, DataSheetAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(DataKey, DataKeyAdmin)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

