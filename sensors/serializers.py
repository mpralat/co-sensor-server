from rest_framework.serializers import ModelSerializer
from .models import SensorData


class SensorDataSerializer(ModelSerializer):

    class Meta:
        model = SensorData
        fields = ('timestamp', 'value')
