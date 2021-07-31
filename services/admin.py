from django.contrib import admin
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


admin.site.register(Template, TemplateAdmin)
admin.site.register(DataSheet, DataSheetAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(DataKey, DataKeyAdmin)

