from accounts.models import *
from dashboard.serializers import CourseBriefSerializer,UserInstallmentSerializer
from rest_framework import serializers


class ShoppingCartSerializer(CourseBriefSerializer):
    installments = UserInstallmentSerializer(source='installment_set',many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('installments','teacher', 'title', 'image')
        depth = 1