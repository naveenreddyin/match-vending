from rest_framework import serializers


class BuySerializer(serializers.Serializer):
    product = serializers.IntegerField()
    amount = serializers.IntegerField()
