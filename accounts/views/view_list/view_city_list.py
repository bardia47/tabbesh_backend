from rest_framework import generics
from accounts.models import City
from accounts.serializers.serializer_list.serializer_list_city import CityListSerializer

class CityListView(generics.ListAPIView):
    serializer_class = CityListSerializer
    queryset = City.objects.all()
