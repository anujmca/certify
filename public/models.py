from django.db import models
from django_tenants.utils import schema_context
from django.conf import settings

from common.models import BaseModel2, BaseTemplate

User = settings.AUTH_USER_MODEL

# import common.models as cm
from certify import settings
from services.models import Event


# class BaseModel(models.Model):
#     """
#     Abstract database model. Extend this to create models.
#     """
#
#     class Meta:
#         abstract = True
#
#     created_on = models.DateTimeField(auto_now_add=True, db_index=True, editable=False,
#                                       help_text='Datetime on which this record was created.')
#     updated_on = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False,
#                                       help_text='Datetime on which this record was last modified.')
#
#     is_deleted = models.BooleanField(null=False, default=False)
#
#     # created_by = models.ForeignKey(User, null=True, related_name='%(class)s_created', on_delete=models.CASCADE)
#     # updated_by = models.ForeignKey(User, null=True, blank=True, related_name='%(class)s_updated',
#     #                                on_delete=models.CASCADE)
#
#     tenant_schema_name = models.CharField(max_length=128, null=False, blank=False, default='public')
#     tenant_created_by_user_id = models.BigIntegerField(null=False, blank=False, default=0)
#     tenant_updated_by_user_id = models.BigIntegerField(null=True, blank=True)
#
#     @property
#     def created_by(self):
#         tenant_created_by = None
#         with schema_context(self.tenant_schema_name):
#             tenant_created_by = User.objects.get(pk=self.tenant_created_by_user_id)
#
#         return tenant_created_by
#
#     @property
#     def updated_by(self):
#         tenant_updated_by = None
#         with schema_context(self.tenant_schema_name):
#             tenant_updated_by = User.objects.get(pk=self.tenant_updated_by_user_id)
#
#         return tenant_updated_by

from django.contrib.auth import get_user_model
UserModel = get_user_model()

from accounts.models import User as BaseUserModel
from django_tenants.utils import schema_context, connection

class PublicUser(BaseUserModel):
    class Meta:
        proxy = True
        # managed = False

    # @property
    # def events(self):
    #     awardee_events = [certificate.event for certificate in PublicCertificate.objects.filter(awardee=self)]
    #     return awardee_events
    #
    # @property
    # def certificates(self):
    #     awardee_certificates = PublicCertificate.objects.filter(awardee=self)
    #     return awardee_certificates

    def get_tenant_specific_events(self, tenant_schema_name):
        awardee_events = [certificate.event for certificate in PublicCertificate.objects.filter(tenant_schema_name=tenant_schema_name, awardee=self)]
        return awardee_events

    def get_tenant_specific_certificates(self, tenant_schema_name):
        awardee_certificates = PublicCertificate.objects.filter(tenant_schema_name=tenant_schema_name, awardee=self)
        return awardee_certificates


class PublicCertificate(BaseModel2):
    awardee = models.ForeignKey(PublicUser, on_delete=models.CASCADE, related_name="public_certificates")
    event_name = models.CharField(max_length=128, null=False, blank=False)
    sms_available = models.BooleanField(null=False, blank=False, default=False)
    email_available = models.BooleanField(null=False, blank=False, default=False)
    sms_sent = models.BooleanField(null=False, blank=False, default=False)
    email_sent = models.BooleanField(null=False, blank=False, default=False)
    file = models.FileField(upload_to='certificates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/certificates/2015/01/30

    # tenant_schema_name = models.CharField(max_length=128)
    tenant_awarded_by_user_id = models.BigIntegerField(null=False, blank=False, default=0)
    tenant_event_id = models.BigIntegerField(null=False, blank=False, default=0)

    @property
    def tenant(self):
        from tenant.models import Client
        return Client.objects.get(name=self.tenant_schema_name)

    @property
    def awarded_to(self):
        awarded_to = None
        with schema_context(settings.PUBLIC_SCHEMA_NAME):
            awarded_to = User.objects.get(pk=self.awardee.id)

        return awarded_to

    @property
    def awarded_by(self):
        tenant_awarded_by = None
        with schema_context(self.tenant_schema_name):
            tenant_awarded_by = User.objects.get(pk=self.tenant_awarded_by_user_id)

        return tenant_awarded_by

    @property
    def event(self):
        event = None
        with schema_context(self.tenant_schema_name):
            event = Event.objects.get(pk=self.tenant_event_id)

        return event

    def __str__(self):
        return str(self.awardee) + ' - ' + self.event_name


class FreeTemplate(BaseTemplate):
    pass
