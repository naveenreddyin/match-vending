from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "seller",
            "amount",
            "cost",
        ]

    def validate_cost(self, value):
        """
        check for multiple of 5 or not else raise exception
        """
        if value % 5 != 0:
            raise serializers.ValidationError("cost is not multiple of 5")
        return value
