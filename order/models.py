from configparser import MAX_INTERPOLATION_DEPTH
from django.db import models
from shop.models import (
    BaseModel,
    ProductOption
)
# Create your models here.
from django.core.validators import RegexValidator
STATUS_CHOICS = (
    ('PENDDING', 'Pendding'),
    ('CONFIRMED', 'Confirmed'),
    ('DELIVERING', 'Delivering'),
    ('DELIVERED', 'Delivered')
)
class Order(BaseModel):

    
    phone_regex = RegexValidator(
        regex=r'/(((\+|)84)|0)(3|5|7|8|9)+([0-9]{8})\b/',
        )
    
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=17)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, 
                              choices=STATUS_CHOICS, 
                              default=STATUS_CHOICS[0][0])
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'Order {self.pk}'
    
    def total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, 
                              related_name='items',
                              on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption,
                                        related_name='order_items',
                                        on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=3, null=True, default=0)
    quantity = models.PositiveIntegerField(default=-1)
    
    def get_cost(self):
        return self.quantity*self.price
    
    def __str__(self):
        return f'{self.id}'