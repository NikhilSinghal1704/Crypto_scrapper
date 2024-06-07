from rest_framework import serializers
from .models import CoinData

class CoinDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinData
        fields = ['coin', 'output']