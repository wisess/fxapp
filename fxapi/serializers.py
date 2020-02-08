from rest_framework import serializers
from . import models

class ComfortZonesSerializer(serializers.ModelSerializer):
    class Meta:
        model 	= models.ComfortZones
        fields 	= ['fx_symbol', 'option_code', 'zone_type', 'start_date', 'end_date', 'call_strike', 'put_strike', 'balance',]

class ComfortZonesGetSerializer(serializers.Serializer):
	symbol = serializers.CharField(required=False)