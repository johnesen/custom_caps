from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from .serializers import *
from .models import *

class OrderListView(generics.ListAPIView):
    """
        Order list
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderListSerializer

class OrderDetView(generics.RetrieveAPIView):
    """
        order deatail view
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderDetailViewSerializer

    # permission_classes = [permissions.IsAdminUsers, permissions.IsAuthenticated]

class OrderItemCreateView(generics.CreateAPIView):
    """
        Order  item create
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer

class OrderCreateView(generics.CreateAPIView):
    """
        Order create
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    # permission_classes = [permissions.IsAdminUsers, permissions.IsAuthenticated]