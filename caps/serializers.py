from rest_framework import serializers
from .models import *

class CapsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapsImage
        fields = ['id', 'photo']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = 'name icon'.split()

class SizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = 'value'.split()

class CapsSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    size = SizesSerializer(read_only=True, many=True)
    capsimage = CapsImageSerializer(read_only=True, many=True)

    class Meta:
        model = Caps
        fields = 'id brand name price size description is_available new_price created_data capsimage'.split()

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = 'id name icon'.split()
