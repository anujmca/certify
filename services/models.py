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
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True, editable=False,
                                       help_text='Datetime on which this record was last modified.')


class Template(BaseModel):
    created_by = models.ForeignKey(User, related_name="templates_created", null=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="templates_updated", null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    # data_sheet = models.FileField(upload_to='data_sheets/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/data_sheets/2015/01/30
    file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/templates/2015/01/30


class DataSheet(BaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=400, null=True)
    data_sheet = models.FileField(upload_to='data_sheets/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/data_sheets/2015/01/30
    template = models.ForeignKey(Template, related_name="data_sheet", null=True, on_delete=models.CASCADE)


class DataKey(BaseModel):
    name = models.CharField(max_length=50, null=False, unique=False)
    value = models.CharField(max_length=200, null=False, unique=False)


class Certificate(BaseModel):
    created_by = models.ForeignKey(User, related_name="certificate_created", null=True, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, related_name="certificates", null=True, on_delete=models.CASCADE)
    batch_id = models.IntegerField()
    data_keys = models.ManyToManyField(DataKey, related_name="certificates", null=True)
    file = models.FileField(upload_to='certificates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/certificates/2015/01/30


import django_tables2 as tables

class CertificateTable(tables.Table):
    class Meta:
        model = Certificate