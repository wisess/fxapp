from rest_framework import generics, views, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import services, serializers


class CabsAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.ComfortZonesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
    	get_serializer = serializers.ComfortZonesGetSerializer(data=request.query_params)
    	get_serializer.is_valid(raise_exception=True)
    	get_data = get_serializer.validated_data
    	qs = services.get_cabs()
    	if 'symbol' in get_data:
    		qs = services.get_cabs(get_data['symbol'].upper())
    	serializer = self.serializer_class(qs, many=True)
    	return Response(serializer.data, status=status.HTTP_200_OK)
