# backend\cart\serializers.py
from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    quantity = serializers.IntegerField(min_value=0)


class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)

