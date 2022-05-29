from rest_framework import generics, permissions, viewsets, mixins
from .serializers import OrderSeralizer
from django_filters import rest_framework as filters
from .models import Order

class OrderViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSeralizer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['status']

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super(OrderViewset, self).get_serializer_context()
        context.update({"request": self.request})
        return context