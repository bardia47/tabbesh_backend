from accounts.models import *
from dashboard.serializers import CourseBriefSerializer, InstallmentSerializer
from rest_framework import serializers
from dashboard.serializers import DiscountSerializer
from accounts.enums import InstallmentModelEnum


class CartInstallmentSerializer(InstallmentSerializer):
    is_bought = serializers.SerializerMethodField('get_is_bought')
    is_disable = serializers.SerializerMethodField('get_is_disable')
    message = serializers.SerializerMethodField('get_message')

    class Meta:
        model = Installment
        fields = ('id', 'title', 'amount', 'start_date', 'end_date', 'is_bought', 'is_disable', 'message')

    def get_is_bought(self, obj):
        if obj.user_set.filter(pk=self.context['request'].user.pk).exists():
            return True
        return False

    def get_is_disable(self, obj):
        now = datetime.datetime.now().date()
        return not ((obj.start_date > now) | (obj.end_date > (now + datetime.timedelta(days=10))))

    def get_message(self, obj):
        if (self.get_is_bought(obj)):
            return InstallmentModelEnum.installmentIsBought.value
        if (self.get_is_disable(obj)):
            return InstallmentModelEnum.installmentIsExpired.value
        return InstallmentModelEnum.installmentIsNotBought.value


class ShoppingCartSerializer(CourseBriefSerializer):
    installments = serializers.SerializerMethodField('get_installments',help_text='get installment not buyed')
    discount = DiscountSerializer(source='get_discount',read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'teacher', 'title', 'image', 'installments', 'discount')
        depth = 1


    def get_installments(self, obj):
        return CartInstallmentSerializer(obj.get_next_installments(exclude={'user__id': self.context['request'].user.id}),context=self.context, many=True).data