
from decimal import Decimal
from functools import reduce
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
    # cart = Cart(request)
    # call is_valid() after add, remove or cart.validate_all()
    # cart.save() if valid otherwise cart data would unchange
    # cart.errors for errors message
    # cart.validate is called in cart.add, cart.remove
    # cart.validate_all() force cart to validate items again

    def __init__(self, request) -> None:
        self.session = request.session
        self.request = request
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
        self.errors = {}
    
    def add(self, product_option, quantity=1, override_quantity=False):
        
        option_id = str(product_option.pk)
        if option_id not in self.cart:
             self.cart[option_id] = self.make_cart_item(product_option, quantity)
        else:
            if override_quantity:
                 self.cart[option_id]['quantity'] = quantity
    
            else:
                self.cart[option_id]['quantity'] += quantity

        # look for erros
        self.catch_error(
            self.validate_quantity, # validator
            self.add_errors,        # error handler
            product_option
            )

    def make_cart_item(self, option, quantity):
        item_option = {
            "product_id": option.specific_product.pk,
            "quantity": quantity,
        } 
        return item_option

    def save(self):
        if self.errors:
            raise Exception('use is_valid to validate before save cart.')
        self.session.modified = True
        
    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True

    @property
    def data(self,
            product_serializer_class=SpecificProductDetailSerializer,
            option_serializer_class=ProductOptionSerializer):

        product_option_ids = self.cart.keys()
        product_options = ProductOption.objects.filter(pk__in=product_option_ids)
        
        for option in product_options:
            option_id = str(option.pk)
            self.cart[option_id]['product_option'] = ProductOptionSerializer(
                option,
                context=self.get_serializer_request_context()
                ).data
            self.cart[option_id]['product'] = SpecificProductDetailSerializer(
                option.specific_product,
                context=self.get_serializer_request_context()
                ).data
            self.cart[option_id]['price'] = str(option.price * self.cart[option_id]['quantity'])
            
        items = self.cart.values()
        prices = list(map(lambda item: Decimal(item['price']), items))
        
        def sum (prev, cur):
            return prev + cur
        total_price = reduce(sum, prices, 0)
        
        return {
            'items': items,
            'total_price': str(total_price),
        }

    def __iter__(self):
        product_option_ids = self.cart.keys()   
        product_options = ProductOption.objects.filter(pk__in=product_option_ids)

        for option in product_options:
            self.cart[str(option.id)]['product_option'] = option
        
        for item in self.cart.values():
            item['price'] = item['product_option'].price
            item['total_price'] = item['price'] * item['quantity']
            yield item
       
    def get_serializer_request_context(self):
        return {
            'request': self.request,
        }
    
    def remove(self, product_option):
        option_id = str(product_option.id)
        if option_id not in self.cart:
            self.add_errors(product_option, 'not in cart')
            return
        del self.cart[option_id]     
    
    def __str__(self) -> str:
        return json.dumps(self.cart)
    
    def is_valid(self):
        return not bool(self.errors)
    
    def add_errors(self, product_option, error):
        option_id = str(product_option.pk)
        self.errors[option_id] = {
            "name": str(product_option),
            "message": str(error)
        }

    def catch_error(self, validator, handler, product_option):
        try:
            validator(product_option)
        except Exception as e:
            return handler(product_option, e)

    def validate_quantity(self, product_option):
        # raise error , else return quantity
        option_id = str(product_option.id)
        if option_id not in self.cart:
            raise Exception(f'{product_option} not in cart')
        if 0 < self.cart[option_id]['quantity'] <= product_option.stock:
            return self.cart[option_id]['quantity']
        raise Exception(f'exceed quantity, only {product_option.stock} left in stock.')
    
    def get_product_options(self):
            product_option_ids = self.cart.keys()
            product_option = ProductOption.objects.filter(pk__in=product_option_ids)
            return product_option

    def validate_all(self):
        options = self.get_product_options()
        (self.catch_error(
            self.validate_quantity,
            self.add_errors,
            option
        ) for option in options)
    
    def is_empty(self):
        return not self.cart.keys()