from rest_framework import serializers

from common.serializers import BaseSerializer
from services.models import *


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'


class EventSerializer(BaseSerializer):
    template = TemplateSerializer(required=False)
    datasheet = DataSheetSerializer(required=False)

    class Meta:
        model = Event
        fields = '__all__'
