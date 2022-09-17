from pyexpat import model
from rest_framework import serializers
from order.models import (
    Order,
    OrderItem
)

from shop.serializers import (
    ProductOptionSerializer,
    SpecificProductDetailSerializer
)

class OrderItem(serializers.ModelSerializer):
    product_option = ProductOptionSerializer()
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        
    def get_product(self, obj):
        return SpecificProductDetailSerializer(obj.product_option.specific_product).data

class OrderSerializerDetail(serializers.ModelSerializer):
    items = OrderItem(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone_number', 'email', 
                  'address', 'city', 'total_price', 'paid', 'status', 'created_at', 
                  'items')
        read_only_fields = ('items', 'paid', 'status', 'total_price')

class OrderSerializer(serializers.ModelSerializer):
    # email = serializers.SerializerMethodField()
    class Meta:
        model = Order   
        fields = ('pk', 'created_at', 'status', 'paid', 'email')
    def get_email(self, obj):
        return self.hide_email(obj.email)
    
    def hide_email(email):
        return email
