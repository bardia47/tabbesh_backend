from accounts.models.grade import Grade
from rest_framework import serializers

class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'