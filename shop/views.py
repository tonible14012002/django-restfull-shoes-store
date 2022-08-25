from math import e
import queue
from time import process_time_ns
from winreg import QueryInfoKey, QueryReflectionKey
from rest_framework import (generics, viewsets)
from .models import (
    AttributeClass,
    SpecificProduct,
    GenericProduct
)
from .serializers import (
    SpecificProductSerializer,
    SpecificProductDetailSerializer,
    GenericProductSerializer,
    AttributeClassSerializer
)

from django.db.models import Q
from functools import reduce
import operator

# Create your views here.
def handle_product_query_string(attr_query=None, price_range_query=None):
    # use try block to ignore incorrect syntax query
    query = None
    try:
        if attr_query:
            attr_str_sets = attr_query.split('^')
            for attr_class in attr_str_sets:
                attrs = attr_class.split(',')
                if query:
                    query &= reduce(
                        operator.or_,
                        (Q(attributes_str__contains=attr) for attr in attrs)
                    )
                else:
                    query = reduce(
                        operator.or_,
                        (Q(attributes_str__contains=attr) for attr in attrs)
                    )
    except Exception as e:
        print(e)
    
    price_query = None
    try:
        if price_range_query:
            price_ranges = price_range_query.split(',')
            def range_converter(q):
                range = q.split('-')
                if len(range) == 1:
                    range.append('9999999')
                if not range[0].isdecimal() or not range[1].isdecimal():
                    raise Exception('query range must be decimal')
                return range
            range_list = list(map(range_converter, price_ranges))
            price_query = reduce(
                operator.or_,
                (Q(product_options__price__range = \
                    (lower, upper)) for lower, upper in range_list)
            )
    except Exception as e:
        print(e)

    if query is None:
        if price_query is None:
            return None
        else:
            return price_query
    elif price_query is None:
        return query
    else:
        return price_query & query


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
        attr_query = self.request.query_params.get('attribute')
        price_range_query = self.request.query_params.get('range')
        query = handle_product_query_string(attr_query, price_range_query)
        if query:
            print(query)
            products = products.filter(
                query
            ).distinct()
        return products

class GenericProductVewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GenericProduct.objects.all()
    serializer_class = GenericProductSerializer
    
class AttributeClassViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = AttributeClass.objects.all()
    serializer_class = AttributeClassSerializer

    