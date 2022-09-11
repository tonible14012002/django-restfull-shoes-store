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
    image = models.ImageField(upload_to='generic_shoes/%y/%m/%d',
                              null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='generic_products')

    def __str__(self):
        return self.name

class AttributeClass(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Attribute(BaseModel):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, default='none')
    attr_class = models.ForeignKey(AttributeClass, 
                                   on_delete=models.CASCADE,
                                   related_name='attributes',
                                   null=True)
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
                                        related_name='specific_products',
                                        null=False, blank=False)
    order_type = models.CharField(choices=ORDER_TYPE_CHOICES,
                                  max_length=50,
                                  default=ORDER_TYPE_CHOICES[0][0])
    attributes = models.ManyToManyField(Attribute, related_name='specific_products')
    attributes_str = models.CharField(max_length=150, blank=True, null=True, default='{}')
    color = models.ForeignKey(Color, related_name='specific_products',
                              on_delete=models.CASCADE,
                              null=True, blank=True)

    class Meta:
        unique_together = ('color', 'name')
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return self.name    
    
class ProductOption(models.Model):
    specific_product = models.ForeignKey(SpecificProduct,
                                         on_delete=models.CASCADE,
                                         related_name='product_options')
    
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.SmallIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=3)
    
    class Meta:
        unique_together = ('specific_product', 'size')
        ordering = ('-price',)
        
    def __str__(self):
        return f'{self.specific_product}-{self.size}'

class ProductMedia(BaseModel):
    product = models.OneToOneField(SpecificProduct,
                                   on_delete=models.CASCADE,
                                   related_name='media')
    def get_two_first(self):
        return self.images.all()[0:2]

    def __str__(self):
        return f'{self.product.name} Media'
    
class ProductImage(BaseModel):
    image = models.ImageField(upload_to='products/%y/%m/%d', null=True)
    media = models.ForeignKey(ProductMedia,
                              on_delete=models.CASCADE,
                              related_name='images')
    class Meta:
        ordering = ('created_at',)