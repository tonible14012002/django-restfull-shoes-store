from email.policy import default
from xmlrpc.client import Boolean
from rest_framework import serializers

class AddCartItemSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
    override_quantity = serializers.BooleanField(default=False)
