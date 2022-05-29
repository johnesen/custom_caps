from rest_framework import serializers
from .models import Order
from caps.models import *
from caps.serializers import CapsSerializer


class OrderSeralizer(serializers.ModelSerializer):
    # item = CapsSerializer()

    class Meta:
        model = Order
        fields = ['id', 'item', 'user', 'order_date', 'price', 'send_date', 'status']
        read_only_fields = ['send_date', 'price', 'status']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request_user = self.context['request'].user
        if data['user'] == request_user.id:
            return data