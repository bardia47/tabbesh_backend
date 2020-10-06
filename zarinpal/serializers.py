from accounts.models import *
from dashboard.serializers import InstallmentSerializer
from rest_framework import serializers


class ShoppingInstallmentSerializer(InstallmentSerializer):
    course = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Installment
        fields = ('id', 'title', 'amount', 'start_date', 'end_date', 'course')
