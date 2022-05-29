from rest_framework import generics, permissions, viewsets, mixins
from .serializers import OrderSeralizer
from .models import Order

class OrderViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSeralizer

    permission_classes = [permissions.IsAuthenticated]