from accounts.models import *
from dashboard.serializers import CourseBriefSerializer, InstallmentSerializer
from rest_framework import serializers
from dashboard.serializers import DiscountSerializer
from accounts.enums import InstallmentModelEnum
from dashboard.serializers import CartInstallmentSerializer
class ShoppingCartSerializer(CourseBriefSerializer):
    installments = serializers.SerializerMethodField('get_installments',help_text='get installment not buyed')
    discount = DiscountSerializer(source='get_discount',read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'teacher', 'title', 'image', 'installments', 'discount')
        depth = 1


    def get_installments(self, obj):
      #  return CartInstallmentSerializer(obj.get_next_installments(exclude={'user__id': self.context['request'].user.id}),context=self.context, many=True).data
      return CartInstallmentSerializer(obj.installment_set.exclude(user=self.context['request'].user.id) ,context=self.context, many=True).data