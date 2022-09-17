from dataclasses import field
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
        exclude = ['created_at', 'updated_at', 'attr_class']

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
        exclude = ['specific_product']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductImage
        exclude = ['media']
        
class SimpleProductMediaSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='get_two_first')
    class Meta:
        model = ProductMedia
        fields = ['images']

class DetailProductMediaSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = ProductMedia
        fields = ['images']

class SpecificProductSerializer(serializers.ModelSerializer):
    
    price_range = serializers.SerializerMethodField()
    color = ColorSerializer(read_only=True)
    attributes = AttributeSerialier(many=True)
    media = SimpleProductMediaSerializer()
    class Meta:
        model = SpecificProduct
        fields = '__all__'
        read_only_fields = ['attribute_str']        
            
    def get_price_range(self, obj):
        price_set = list(map(
            lambda option:option.price, 
            obj.product_options.all()
        ))
        return f'{min(price_set)} - {max(price_set)}'

class GenericProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    specific_products = SpecificProductSerializer(many=True)
    class Meta: 
        model = GenericProduct
        fields = ['name', 'details', 'categories', 'specific_products']
        
class SpecificProductDetailSerializer(SpecificProductSerializer):
    media = DetailProductMediaSerializer()
    product_options = ProductOptionSerializer(many=True)
    generic_product = GenericProductSerializer()
    class Meta:
        model = SpecificProduct
        fields = ['id', 'name', 'generic_product', 'product_options', 'media',
                  'order_type', 'color', 'updated_at', 'created_at', 'price_range']


class AttributeClassSerializer(serializers.ModelSerializer):
    attributes = AttributeSerialier(many=True)
    class Meta:
        model = AttributeClass
        fields = ['id', 'name', 'attributes']