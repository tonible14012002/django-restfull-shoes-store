from pyexpat import model
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttributeSerialier(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ['created_at', 'updated_at']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ['created_at', 'updated_at']
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ['created_at', 'updated_at']
        
class ProductOptionSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    class Meta:
        model = ProductOption
        fields = '__all__'

class SpecificProductDetailSerializer(serializers.ModelSerializer):
    product_option_set = ProductOptionSerializer(many=True)
    color = ColorSerializer()
    class Meta:
        model = SpecificProduct
        fields = ['name', 'generic_product', 'product_option_set', 'order_type', 'color', 'updated_at', 'created_at']

class SpecificProductSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    attributes = AttributeSerialier(many=True)
    class Meta:
        model = SpecificProduct
        fields = '__all__'

class GenericProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    class Meta:
        model = GenericProduct
        fields = '__all__'
