from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.postgres.fields import ArrayField

from certify import settings
from services import utilities
from django.core.files import File
from django_tenants.utils import schema_context



class BaseModel(models.Model):
    """
    Abstract database model. Extend this to create models.
    """

    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True, db_index=True, editable=False,
                                      help_text='Datetime on which this record was created.')
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False,
                                      help_text='Datetime on which this record was last modified.')

    created_by = models.ForeignKey(User, null=True, related_name='%(class)s_created', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='%(class)s_updated',
                                   on_delete=models.CASCADE)

    is_deleted = models.BooleanField(null=False, default=False)

    # def save(self, user, *args, **kwargs):
    #     user = user
    #     super().save(*args, **kwargs)


class BaseModel2(models.Model):
    """
    Abstract database model. Extend this to create models.
    """

    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True, db_index=True, editable=False,
                                      help_text='Datetime on which this record was created.')
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False,
                                      help_text='Datetime on which this record was last modified.')

    is_deleted = models.BooleanField(null=False, default=False)

    # created_by = models.ForeignKey(User, null=True, related_name='%(class)s_created', on_delete=models.CASCADE)
    # updated_by = models.ForeignKey(User, null=True, blank=True, related_name='%(class)s_updated',
    #                                on_delete=models.CASCADE)

    tenant_schema_name = models.CharField(max_length=128, null=False, blank=False, default='public')
    tenant_created_by_user_id = models.BigIntegerField(null=False, blank=False, default=0)
    tenant_updated_by_user_id = models.BigIntegerField(null=True, blank=True)

    @property
    def created_by(self):
        tenant_created_by = None
        with schema_context(self.tenant_schema_name):
            tenant_created_by = User.objects.get(pk=self.tenant_created_by_user_id)

        return tenant_created_by

    @property
    def updated_by(self):
        tenant_updated_by = None
        with schema_context(self.tenant_schema_name):
            tenant_updated_by = User.objects.get(pk=self.tenant_updated_by_user_id)

        return tenant_updated_by

# class CommonProfile(BaseModel):
#     phone_number = models.CharField(max_length=100, null=False, unique=True)
#     client_user_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
#     otp = models.CharField(max_length=10, null=True, blank=True, unique=False, )
#     otp_valid_till = models.DateTimeField(null=True, blank=True, editable=True, help_text="UTC Time")

