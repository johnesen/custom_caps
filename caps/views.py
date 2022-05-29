from caps.models import Caps, Brand
from rest_framework import generics, permissions
from .serializers import BrandListSerializer, CapsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics, permissions, viewsets, mixins


class CapsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Caps.available.all()
    serializer_class = CapsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'brand__name', 'price', 'brand__name']
    ordering_fields = 'price created_data'.split()

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [permissions.AllowAny]


class BrandCapListAPIView(ListModelMixin, GenericAPIView): 
    queryset = Caps.available.all()
    serializer_class = CapsSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug_url = self.kwargs['slug_url']
        return Caps.available.filter(brand__slug=slug_url)
