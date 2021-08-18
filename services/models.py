from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


from certify import settings
from services import utilities


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
    file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/templates/2015/01/30
    tokens = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tokens = utilities.get_ppt_tokens(self.file)
        super(Template, self).save(*args, **kwargs)



class DataSheet(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    data_sheet = models.FileField(
        upload_to='data_sheets/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/data_sheets/2015/01/30
    # template = models.ForeignKey(Template, related_name="data_sheet", null=True, on_delete=models.CASCADE)
    tokens = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        tokens = utilities.get_excel_headers(self.data_sheet)
        self.tokens = list()
        for token in tokens:
            self.tokens.append(token)
        super(DataSheet, self).save(*args, **kwargs)

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

    @property
    def status(self):
        status = None
        if (self.name and self.awarded_by):
            if self.template is None:
                status = settings.EVENT_STATUS.PENDING_TEMPLATE
            elif self.datasheet is None:
                status = settings.EVENT_STATUS.PENDING_DATASHEET
            # elif self.payment is None:
            #     status = settings.EVENT_STATUS.PENDING_PAYMENT
            elif not self.template.tokens.__eq__(self.datasheet.tokens):
                status = settings.EVENT_STATUS.INVALID_DATA_KEYS
            else:
                status = settings.EVENT_STATUS.READY_TO_GENERATE
        return status


# import django_tables2 as tables
#
# class CertificateTable(tables.Table):
#     class Meta:
#         model = Certificate
