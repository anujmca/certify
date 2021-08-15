from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


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


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=100, null=False, unique=True)
    otp = models.CharField(max_length=10, null=True, blank=True, unique=False, )
    otp_valid_till = models.DateTimeField(null=True, blank=True, editable=True, help_text="UTC Time")

    def __str__(self):
        return self.user.email


class Template(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    # data_sheet = models.FileField(upload_to='data_sheets/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/data_sheets/2015/01/30
    file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/templates/2015/01/30

    def __str__(self):
        return self.name


class DataSheet(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    data_sheet = models.FileField(
        upload_to='data_sheets/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/data_sheets/2015/01/30
    template = models.ForeignKey(Template, related_name="data_sheet", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataKey(BaseModel):
    name = models.CharField(max_length=50, null=False, unique=False)
    value = models.CharField(max_length=200, null=False, unique=False)

    def __str__(self):
        return self.name


class Certificate(BaseModel):
    created_by = models.ForeignKey(User, related_name="certificate_created", null=True, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, related_name="certificates", null=True, on_delete=models.CASCADE)
    batch_id = models.IntegerField()
    data_keys = models.ManyToManyField(DataKey, related_name="certificates")
    file = models.FileField(
        upload_to='certificates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/certificates/2015/01/30


class Event(BaseModel):
    name = models.CharField(max_length=100, null=False)
    awarded_by = models.CharField(max_length=100, null=False)
    template = models.ForeignKey(Template, related_name="events", null=True, blank=True, on_delete=models.CASCADE)
    datasheet = models.ForeignKey(DataSheet, related_name="events", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



# import django_tables2 as tables
#
# class CertificateTable(tables.Table):
#     class Meta:
#         model = Certificate
