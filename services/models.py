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


class Templates(BaseModel):
    created_by = models.OneToOneField(User, related_name="templates_created", on_delete=models.CASCADE)
    updated_by = models.OneToOneField(User, related_name="templates_updated", on_delete=models.CASCADE)
    name = models.TextField(null=False, unique=True)
    file = models.FileField(upload_to='templates/%Y/%m/%d/')  # file will be saved to MEDIA_ROOT/uploads/2015/01/30
