from rest_framework import generics, views, exceptions, permissions, status
from rest_framework.response import Response
from . import models, serializers


class WeeklyComfortZoneAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.ComfortZonesSerializer

    def get_queryset(self):
    	return models.ComfortZones.objects

    def get(self, request, *args, **kwargs):
    	qs = self.get_queryset()
    	serializer = self.serializer_class(qs, many=True)
    	return Response(serializer.data, status=status.HTTP_200_OK)
