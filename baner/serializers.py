from rest_framework import serializers
from . import models
from caps.serializers import CapsImageSerializer
from caps.models import Caps

class CapsListViewSerializers(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    capsimage = CapsImageSerializer(many=True)
    class Meta:
        model = Caps
        fields = 'id brand name price new_price capsimage'.split()



class BanerViewSerialiser(serializers.ModelSerializer):
    # caps = CapsListViewSerializers(many=True)
    class Meta:
        model = models.Baner
        fields = ['id', 'baner_title', 'baner']