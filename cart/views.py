from copyreg import constructor
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
    AddCartItemSerializer,
)
# Create your views here.

class CartViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():                
            data = serializer.data
            option = ProductOption.objects.get(
                pk=data['option_id'],
            ) 

            cart = Cart(request)
            cart.add(
                product_option=option,
                quantity=data['quantity'],
                override_quantity=data['override_quantity']
            )
            
            if cart.is_valid():
                cart.save()
                return Response(cart.data, status=status.HTTP_200_OK)
            return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        cart = Cart(request)
        return Response(cart.data)

    def destroy(self, request, pk):
        product_option = ProductOption.objects.get(pk=pk)
        cart = Cart(request)
        cart.remove(product_option)
        if cart.is_valid():
            cart.save()
            return Response(cart.data, status=status.HTTP_200_OK)
        return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)        
