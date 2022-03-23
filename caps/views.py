from django.db import models
from rest_framework.response import Response
from caps.models import *
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .serializers import (
    BrandListSerializer,
    CapsListViewSerializers, 
    CapsCreateViewSerializers, 
    UserCapsFavoriteSerializer,
    FavouriteSerializer,
    CapsDetailSerializer,
    BasketListSerializer, 
    BasketDetailSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as flters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User




class CapsListView(generics.ListAPIView):
    """
        views for print CAPS LIST
    """
    queryset = Caps.available.all()
    serializer_class = CapsListViewSerializers
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'brand__name', 'price', 'brand__name']
    ordering_fields = 'price created_data'.split()


class CapsCreateView(generics.CreateAPIView):
    """
        ciews for CREATE CAP
    """
    queryset = Caps.available.all()
    serializer_class = CapsCreateViewSerializers
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticated]


class BrandListView(generics.ListAPIView):
    """
        Views for print BRAND LIST
    """
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.AllowAny]


class BrandCapListAPIView(ListModelMixin, GenericAPIView): 
    """
        Views for SORT CAPS BY BRAND
    """
    # queryset = Caps.available.all()
    serializer_class = CapsListViewSerializers
    permission_classes = [
        permissions.IsAdminUser, permissions.AllowAny]
    def get_queryset(self):
        slug_url = self.kwargs['slug_url']
        return Caps.available.filter(brand__slug=slug_url)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FavouriteListView(generics.ListCreateAPIView):
    """
        favorite caps list 
    """
    queryset = UserCapsFavorite.objects.all()
    serializer_class = FavouriteSerializer

    def pre_sve(self, obj):
        obj.user = self.request.user


class FavouriteDeailView(generics.RetrieveUpdateDestroyAPIView):
    """
        deatil view cap in favorite
    """
    queryset = UserCapsFavorite.objects.all()
    serializer_class = FavouriteSerializer

    def pre_sve(self, obj):
        obj.user = self.request.user


class CapDetailAPIView(generics.RetrieveAPIView):
    """ 
        Детальной информации кепок
     """
    queryset = Caps.available.all()
    serializer_class = CapsDetailSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.AllowAny]

class BasketListView(generics.ListAPIView):
    """
        список корзин
    """
    queryset = Basket.objects.all()
    serializer_class = BasketListSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]

class BasketDetailView(generics.RetrieveAPIView):
    """
        детальный вид корзины
    """
    queryset = Basket.objects.all()
    serializer_class = BasketDetailSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]
