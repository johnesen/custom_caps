from rest_framework import serializers
from .models import CapsInDigit


class InDigitViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapsInDigit
        fields = ['id', 'saled', 'year_in_market', 'clients']

