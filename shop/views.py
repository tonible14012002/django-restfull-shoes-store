import queue
from time import process_time_ns
from rest_framework import (generics, viewsets)
from .models import (
    SpecificProduct,
    GenericProduct
)
from .serializers import (
    SpecificProductSerializer,
    SpecificProductDetailSerializer,
    GenericProductSerializer
)

from django.db.models import Q
from functools import reduce
import operator

# Create your views here.


class SpecificProductViewSet(viewsets.ViewSet,
                             generics.ListAPIView, 
                             generics.RetrieveAPIView):
    queryset = SpecificProduct.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpecificProductDetailSerializer
        return SpecificProductSerializer
    
    def get_queryset(self):
        products = super().get_queryset()
        attr_str = self.request.query_params.get('attribute')
        if attr_str is not None:
            if ',' in attr_str:
                attribute_list = attr_str.split(',')
            else:
                attribute_list = [attr_str]
            query = reduce(operator.or_, (Q(attributes__name__icontains=attr) for attr in attribute_list))
            print(query)
            products = SpecificProduct.objects.filter(
                query
            )
        return products

class GenericProductVewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GenericProduct.objects.all()
    serializer_class = GenericProductSerializer