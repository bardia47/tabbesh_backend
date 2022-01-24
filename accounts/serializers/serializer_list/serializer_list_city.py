from accounts.models.city import City
from rest_framework import serializers

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'code', 'title')
