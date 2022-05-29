from rest_framework import generics, permissions
from baner import serializers
from baner.models import Baner


class BanerListView(generics.ListAPIView):
    queryset = Baner.objects.all().order_by('-id')
    serializer_class = serializers.BanerViewSerialiser
    