from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.get_fields()]
    search_fields = ['name']

@admin.register(GenericProduct)
class GenericProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'get_categories', 'created_at', 'updated_at']
    
    def get_categories(self, obj):
        return ' - '.join([cate.name for cate in obj.categories.all()])

class GenericProductInline(admin.StackedInline):
    model = GenericProduct

@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['get_specific_product', 'get_size', 'stock', 'price']
    
    def get_specific_product(self,obj):
        return obj.specific_product
    def get_size(self, obj):
        return obj.size
        
class ProductOptionInline(admin.StackedInline):
    model = ProductOption    

class ProductMediaInline(admin.StackedInline):
    model = ProductMedia

class ProductImageInline(admin.StackedInline):
    model = ProductImage

@admin.register(SpecificProduct)
class SpecificProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'order_type', 'get_generic_product' , 'created_at', 'updated_at', 'get_colors', 'attributes_str']
    readonly_fields = ['attributes_str']
    inlines = [ProductOptionInline, ProductMediaInline]
    def get_generic_product(self, obj):
        return obj.generic_product
    def get_colors(self, obj):
        return obj.color

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']

class AttributeInline(admin.StackedInline):
    model = Attribute

@admin.register(AttributeClass)
class AttributeClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [AttributeInline]

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'value']