from accounts.models import *
from dashboard.serializers import CourseBriefSerializer, UserInstallmentSerializer
from rest_framework import serializers
from dashboard.serializers import DiscountSerializer

class ShoppingCartSerializer(CourseBriefSerializer):
    installments = UserInstallmentSerializer(source='installment_set', many=True, read_only=True)
    discount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Course
        fields = ('id', 'teacher', 'title', 'image', 'installments', 'discount')
        depth = 1

    def get_discount(self, obj):
        discount = obj.get_discount()
        if discount:
            return DiscountSerializer(instance=discount).data
        return None