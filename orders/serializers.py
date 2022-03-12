from rest_framework import serializers
from .models import Status, OrderItem, Order
from caps.models import *
from caps.serializers import BasketDetailSerializer


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["status"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_date"]

class OrderDetailSeralizer(serializers.ModelSerializer):
    basket = BasketDetailSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['basket', 'order_date']

class OrderListSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id", "order_code", "status", "order"]


class OrderDetailViewSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field='status', read_only=True)
    order = OrderDetailSeralizer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'price', 'send_date', 'order', 'order_code','status']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['basket']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = 'order_code order status price send_date'.split()