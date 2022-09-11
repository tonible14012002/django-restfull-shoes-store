from math import prod
from shutil import ExecError
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import (
    ObjectDoesNotExist
)

from shop.models import (
    SpecificProduct,
    ProductOption
)
from .cart import Cart
from .serializers import (
    AddCartItemSerializer
)
# Create your views here.

class CartViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():                
            try:
                data = serializer.data
                option = ProductOption.objects.get(
                    pk=data['option_id'],
                ) 
                
                cart = Cart(request)
                
                in_cart_quantity = cart.get_quantity(option)
                if data['override_quantity'] and data['quantity'] > option.stock:
                    raise Exception(f'only {option.stock} products left in stock')
                elif not data['override_quantity'] \
                    and (data['quantity'] + in_cart_quantity) > option.stock:
                    raise Exception(f'only {option.stock} products left in stock')
                
                cart.add(
                    product_option=option,
                    quantity=data['quantity'],
                    override_quantity=data['override_quantity']
                )
                return Response(cart.dict, status=status.HTTP_200_OK)
            except (ObjectDoesNotExist, Exception) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        cart = Cart(request)
        return Response(cart.dict)

    def destroy(self, request, pk):
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():                
            try:
                data = serializer.data
                option = ProductOption.objects.get(
                    pk=pk
                ) 
                
                cart = Cart(request)
                
                in_cart_quantity = cart.get_quantity(option)
                if in_cart_quantity - data['quantity'] < 0:
                    raise Exception(f'Only {in_cart_quantity} items in cart')

                cart.remove(
                    product_option=option,
                    quantity=data['quantity'],
                )
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except (ObjectDoesNotExist, Exception) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
