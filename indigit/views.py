from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CapsInDigit
from .serializers import InDigitViewSerializer


class IndigitView(generics.ListAPIView):
    queryset = CapsInDigit.objects.all()
    serializer_class = InDigitViewSerializer
    pagination_class = None 