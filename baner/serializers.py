from rest_framework import serializers
from . import models

class BanerViewSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.Baner
        fields = ['id', 'baner_title', 'baner']