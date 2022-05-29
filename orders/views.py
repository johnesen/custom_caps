from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.generics import GenericAPIView
from .serializers import *
from .models import *

class OrderListView(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class OrderDetView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderDetailViewSerializer

    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class OrderItemCreateView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]