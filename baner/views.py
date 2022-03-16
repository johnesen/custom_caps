from rest_framework import generics, permissions
from baner import serializers

from baner.models import Baner


class BanerListView(generics.ListAPIView):
    """
        list of baners
    """
    queryset = Baner.objects.all()
    serializer_class = serializers.BanerViewSerialiser
