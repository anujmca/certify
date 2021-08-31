from rest_framework import serializers
from services.models import *


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = '__all__'
        # read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by')

