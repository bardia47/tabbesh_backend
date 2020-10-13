from accounts.models import *
from dashboard.serializers import CourseBriefSerializer, InstallmentSerializer
from rest_framework import serializers
from dashboard.serializers import DiscountSerializer
from accounts.enums import InstallmentModelEnum


class CartInstallmentSerializer(InstallmentSerializer):
    is_bought = serializers.SerializerMethodField('get_is_bought')
    is_disable = serializers.SerializerMethodField('get_is_disable')
    amount = serializers.ReadOnlyField(source='get_amount_payable', help_text='مبلغ با احتساب تخفیف')
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
    installments = CartInstallmentSerializer(source='get_next_installments', many=True, read_only=True)
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
