from rest_framework import serializers

from common.serializers import BaseSerializer
from .models import *


class PublicCertificateSerializer(BaseSerializer):
    class Meta:
        model = PublicCertificate
        fields = '__all__'
