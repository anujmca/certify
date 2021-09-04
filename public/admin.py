from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

#
# class PublicProfileAdmin(admin.ModelAdmin):
#     model = Profile
#     # readonly_fields = ['otp_valid_till']


class PublicCertificateAdmin(admin.ModelAdmin):
    model = PublicCertificate


# admin.site.register(Profile, PublicProfileAdmin)
admin.site.register(PublicCertificate, PublicCertificateAdmin)


class FreeTemplateAdmin(admin.ModelAdmin):
    model = FreeTemplate


admin.site.register(FreeTemplate, FreeTemplateAdmin)


# class PublicProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'PublicProfile'
#     fk_name = 'user'
#
#
# class CustomUserAdmin(UserAdmin):
#     inlines = (PublicProfileInline, )
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)
#
#
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
