from rest_framework import serializers
from .models import Status, OrderItem, Order
from caps.models import *
from caps.serializers import BasketDetailSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["status"]

class OrderSeralizer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    basket = BasketDetailSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'basket', 'order_date', 'price', 'send_date','status']
