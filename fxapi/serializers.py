from rest_framework import serializers
from . import models

class ComfortZonesSerializer(serializers.ModelSerializer):
    class Meta:
        model 	= models.ComfortZones
        fields 	= '__all__'
