from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from cart.cart import Cart
from .models import (
    Order,
    OrderItem
)
from .serializers import (
    OrderSerializer,
    OrderSerializerDetail
)
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class OrderViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend] #  equality-based filtering
    filterset_fields = ['id', 'email', 'phone_number']

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderSerializer
        return OrderSerializerDetail

    def get_object(self):
        return super().get_object()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            cart = Cart(request)
            if cart.is_empty():
                return Response("Your cart is empty",
                                status=status.HTTP_400_BAD_REQUEST)
            cart.validate_all()
            if cart.is_valid():
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product_option=item['product_option'],
                        quantity=item['quantity'],
                        price=item['price']
                        )
                cart.clear()
                return Response(OrderSerializerDetail(order).data, status=status.HTTP_200_OK)
            return Response(cart.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    