from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
PublicUser = get_user_model()
from django.contrib.postgres.fields import ArrayField

from certify import settings
from common.models import BaseModel
from services import utilities
from django.core.files import File
from django_tenants.utils import schema_context



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
#     created_by = models.ForeignKey(User, null=True, related_name='%(class)s_created', on_delete=models.CASCADE)
#     updated_by = models.ForeignKey(User, null=True, blank=True, related_name='%(class)s_updated',
#                                    on_delete=models.CASCADE)
#
#     is_deleted = models.BooleanField(null=False, default=False)
#
#


class Template(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/templates/2015/01/30
    tokens = ArrayField(models.CharField(max_length=50), blank=True, null=True, default=None)
    # pdf_file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/templates/2015/01/30
    # file_jpg = models.FileField(upload_to='templates/%Y/%m/%d/', blank=True, null=True)  # file will be saved to MEDIA_ROOT/templates/2015/01/30

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tokens = utilities.get_ppt_tokens(self.file)
        super(Template, self).save(*args, **kwargs)

        # jpg_file_path = utilities.get_jpg_file(self.file)
        #
        # if jpg_file_path is not None:
        #     reopen = open(jpg_file_path, 'rb')
        #     django_file = File(reopen)
        #     # self.file_jpg.save('abc.jpg', django_file, save=True)
        #     reopen.close()


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


class Event(BaseModel):
    name = models.CharField(max_length=100, null=False)
    awarded_by = models.CharField(max_length=100, null=False)
    template = models.ForeignKey(Template, related_name="events", null=True, blank=True, on_delete=models.CASCADE)
    datasheet = models.ForeignKey(DataSheet, related_name="events", null=True, blank=True, on_delete=models.CASCADE)

    awardee_count = models.IntegerField(null=True, blank=True, default=0)
    are_certificates_generated = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.name

    @property
    def status(self):
        status = None
        if not self.are_certificates_generated:
            if (self.name and self.awarded_by):
                if self.template is None:
                    status = settings.EVENT_STATUS.PENDING_TEMPLATE
                elif self.datasheet is None:
                    status = settings.EVENT_STATUS.PENDING_DATASHEET
                # elif self.payment is None:
                #     status = settings.EVENT_STATUS.PENDING_PAYMENT
                elif not set(utilities.DEFAULT_TOKENS).issubset(set(self.datasheet.tokens)):
                    status = settings.EVENT_STATUS.INVALID_DATA_KEYS
                elif not set(self.template.tokens).issubset(set(self.datasheet.tokens)):
                    status = settings.EVENT_STATUS.MISMATCHING_KEYS
                else:
                    status = settings.EVENT_STATUS.READY_TO_GENERATE
        else:
            status = settings.EVENT_STATUS.CERTIFICATE_GENERATED
        return status

    @property
    def certificate_generated_count(self):
        return 0 if self.certificates is None else self.certificates.count()

    @property
    def sms_available_count(self):
        return len(self.certificates.filter(sms_available__exact=True))

    @property
    def email_available_count(self):
        return len(self.certificates.filter(email_available__exact=True))

    @property
    def sms_sent_count(self):
        return len(self.certificates.filter(sms_sent__exact=True))

    @property
    def email_sent_count(self):
        return len(self.certificates.filter(email_sent__exact=True))


class Certificate(BaseModel):
    class STATUSES(models.TextChoices):
        UNPUBLISHED = 'UN', 'Unpublished'
        PUBLISHED = 'PB', 'Published'

    # awardee = models.ForeignKey(User, related_name="certificates", null=True, blank=True, on_delete=models.CASCADE)
    awardee_public_id = models.BigIntegerField(null=True, blank=True, default=None) # Kept it nullable to allow creating certificates without user
    event = models.ForeignKey(Event, related_name="certificates", null=False, blank=False, on_delete=models.CASCADE)
    batch_id = models.IntegerField()
    data_keys = models.ManyToManyField(DataKey, related_name="certificates")
    sms_available = models.BooleanField(null=False, blank=False, default=False)
    email_available = models.BooleanField(null=False, blank=False, default=False)
    sms_sent = models.BooleanField(null=False, blank=False, default=False)
    email_sent = models.BooleanField(null=False, blank=False, default=False)
    status = models.CharField(
        max_length=2,
        choices=STATUSES.choices,
        default=STATUSES.UNPUBLISHED,
        null=False, blank=False,
    )
    file = models.FileField(
        upload_to='certificates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/certificates/2015/01/30

    @property
    def awardee(self):
        result = None
        if self.awardee_public_id is not None and self.awardee_public_id > 0:
            with schema_context(settings.PUBLIC_SCHEMA_NAME):
                result = PublicUser.objects.get(pk=self.awardee_public_id)

        return result
# import django_tables2 as tables
#
# class CertificateTable(tables.Table):
#     class Meta:
#         model = Certificate
