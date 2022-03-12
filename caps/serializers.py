from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CapsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapsImage
        fields = ['image']

class CapsListViewSerializers(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    capsimage = CapsImageSerializer(many=True)
    class Meta:
        model = Caps
        fields = 'id brand name price new_price capsimage is_available'.split()




class CapsCreateViewSerializers(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = Caps
        fields = 'id brand name price new_price is_available'.split()

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = 'id name icon'.split()


class UserCapsFavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    caps = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = UserCapsFavorite
        fields = 'user caps is_favorite'.split()



class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCapsFavorite
        fields = ('id', 'user', 'caps', 'is_favorite')



class SizesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = 'id value'.split()


class CapsDetailSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    size = SizesListSerializer(read_only=True, many=True)

    class Meta:
        model = Caps
        fields = '__all__'


class BasketListSerializer(serializers.ModelSerializer):
    # item = serializers.SlugRelatedField(slug_field='name', read_only=True)
    item = CapsDetailSerializer(read_only=True)
    class Meta:
        model = Basket
        fields = 'id item'.split()

class BasketDetailSerializer(serializers.ModelSerializer):
    size = serializers.SlugRelatedField(slug_field='value', read_only=True)
    item = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Basket
        fields = '__all__'