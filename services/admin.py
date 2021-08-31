from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from services.models import *


class BaseAdmin(admin.ModelAdmin):
    model = BaseModel
    readonly_fields = ('created_on', 'updated_on', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user

        obj.save()

class TemplateAdmin(admin.ModelAdmin):
    model = Template


class DataSheetAdmin(admin.ModelAdmin):
    model = DataSheet


class CertificateAdmin(admin.ModelAdmin):
    model = Certificate


class DataKeyAdmin(admin.ModelAdmin):
    model = DataKey


# class ProfileAdmin(admin.ModelAdmin):
#     model = Profile
#     # readonly_fields = ['otp_valid_till']

class EventAdmin(admin.ModelAdmin):
    model = Event


# admin.site.register(Profile, ProfileAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(DataSheet, DataSheetAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(DataKey, DataKeyAdmin)
admin.site.register(Event, EventAdmin)


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
#
#
# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)
#
#
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

