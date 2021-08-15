from rest_framework import serializers
from services.models import *


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = '__all__'
        # read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by')


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
