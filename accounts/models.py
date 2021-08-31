from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django_tenants.utils import schema_context
from django.db import models


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


class User(AbstractUser, BaseModel2):
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    otp = models.CharField(max_length=10, null=True, blank=True, unique=False, )
    otp_valid_till = models.DateTimeField(null=True, blank=True, editable=True, help_text="UTC Time")

    def __str__(self):
        return self.email

#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, phone_number=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#         )
#
#         user.set_password(password)
#         user.phone_number = None
#         user.save(using=self._db)
#         return user
#
#     def create_staffuser(self, email, password):
#         """
#         Creates and saves a staff user with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user
