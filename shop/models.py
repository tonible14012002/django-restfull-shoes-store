from msilib.schema import SelfReg
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Category(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class GenericProduct(BaseModel):
    name = models.CharField(max_length=100)
    details = models.TextField()
    image = models.ImageField(upload_to='generic_shoes/%y/%m/%d')
    categories = models.ManyToManyField(Category, related_name='generic_products')

    def __str__(self):
        return self.name

class Attribute(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    
class Size(BaseModel):
    SIZE_CHOICES = ((str(i), str(i)) for i in range(35,46))
    size = models.CharField(choices=SIZE_CHOICES,
                            max_length=50, unique=True)
    details = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.size

class Color(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    color_code = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class SpecificProduct(BaseModel):

    ORDER_TYPE_CHOICES = (
        ('ready', 'Ready'),
        ('preoder', 'Preoder'),
    )
    
    name = models.CharField(max_length=100)
    generic_product = models.ForeignKey(GenericProduct,
                                        on_delete=models.CASCADE,
                                        related_name='specific_product',
                                        null=False, blank=False)
    order_type = models.CharField(choices=ORDER_TYPE_CHOICES,
                                  max_length=50,
                                  default=ORDER_TYPE_CHOICES[0][0])
    attributes = models.ManyToManyField(Attribute, related_name='specific_products')
    color = models.ForeignKey(Color, related_name='specific_products',
                              on_delete=models.CASCADE,
                              null=True, blank=True)

    class Meta:
        unique_together = ('color', 'name')

    def __str__(self):
        return self.name    
    
class ProductOption(models.Model):
    specific_product = models.ForeignKey(SpecificProduct,
                                         on_delete=models.CASCADE,
                                         related_name='product_option_set')
    
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.SmallIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=3)
    
    class Meta:
        unique_together = ('specific_product', 'size')
        
    def __str__(self):
        return f'{self.specific_product}-{self.size}'