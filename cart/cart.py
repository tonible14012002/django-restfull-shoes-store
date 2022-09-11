from functools import reduce
import json
from decimal import Decimal
from math import prod
from multiprocessing import context
import re
from shop.models import (
    ProductOption,
    SpecificProduct
)

from shop.serializers import (
    ProductOptionSerializer,
    SpecificProductDetailSerializer
)
from time import sleep


CART_SESSION_ID = 'cart'

class Cart():

    def __init__(self, request) -> None:
        sleep(1)
        self.session = request.session
        self.request = request
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product_option, quantity=1, override_quantity=False):
        
        option_id = str(product_option.pk)
        if option_id not in self.cart:
             self.cart[option_id] = self.make_cart_item_option(product_option, quantity)
        else:
            if override_quantity:
                 self.cart[option_id]['quantity'] = quantity
    
            else:
                self.cart[option_id]['quantity'] += quantity
                
            if self.cart[option_id]['quantity'] > product_option.stock:
                self.cart[option_id]['quantity']= product_option.stock
            
        self.save()
    
    def make_cart_item_option(self, option, quantity):
        item_option = {
            "product_id": option.specific_product.pk,
            "price": str(option.price),
            "quantity": quantity,
        } 
        return item_option

    def save(self):
        self.session.modified = True
        
    def get_option_price(self, option):
        option_id = str(option.pk)
        price = self.cart[option_id]['price']
        quantity = self.cart[option_id]['quantity']
        return Decimal(price)*quantity

    @property
    def dict(self,
                product_serializer_class=SpecificProductDetailSerializer,
                option_serializer_class=ProductOptionSerializer):
        product_option_ids = self.cart.keys()

        item_list = []
        options_price = []
        for option_id in product_option_ids:
            product_option = ProductOption.objects.get(pk=option_id)
            price = self.get_option_price(product_option)
            item = {
                'option': ProductOptionSerializer(
                    product_option, 
                    context=self.get_serializer_request_context()
                ).data,
                'product': SpecificProductDetailSerializer(
                    product_option.specific_product, 
                    context=self.get_serializer_request_context()
                ).data,
                'quantity': self.cart[option_id]['quantity'],
                'price': price
            }
            item_list.append(item)
            options_price.append(price)
        return {
            'items': item_list,
            'total_price': str(sum(options_price))
        }

    def get_quantity(self, option):
        option_id = str(option.pk)
        option_in_cart = self.cart.get(option_id)
        if option_in_cart is not None:
            return option_in_cart['quantity']
        return 0
    
    def get_serializer_request_context(self):
        return {
            'request': self.request,
        }
    
    def remove(self, product_option, quantity):
        option_id = str(product_option.pk)
        if option_id not in self.cart:
            return False
        self.cart[option_id]['quantity'] -= quantity
        if self.cart[option_id]['quantity'] <= 0:
            del self.cart[option_id]
        self.save()