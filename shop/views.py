from rest_framework import (generics, viewsets)

from cart.cart import Cart
from .models import (
    AttributeClass,
    Category,
    SpecificProduct,
    GenericProduct
)
from .serializers import (
    CategorySerializer,
    SpecificProductSerializer,
    SpecificProductDetailSerializer,
    GenericProductSerializer,
    AttributeClassSerializer,
)

from django.db.models import Q
from functools import reduce
import operator
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response

def sleep(timer):
    time.sleep(timer)
    return
# Create your views here.
def make_query_by_attr(attr_query):
    if not attr_query:
        return None
    
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
        return None
    return query

def make_query_by_price_range(price_range_query):
    if not price_range_query:
        return None
    
    query = None
    try:
        price_ranges = price_range_query.split(',')
        def range_converter(q):
            range = q.split('-')
            if len(range) == 1:
                range.append('9999999')
            if not range[0].isdecimal() or not range[1].isdecimal():
                raise Exception('query range must be decimal')
            return range
        range_list = list(map(range_converter, price_ranges))
        query = reduce(
            operator.or_,
            (Q(product_options__price__range = \
                (lower, upper)) for lower, upper in range_list)
        )
    except Exception as e:
        print(e)
        return None
    return query

def make_query_by_category(cate_query):
    if not cate_query:
        return None

    query = None
    try:
        cates = cate_query.split(',')
        query = reduce(
            operator.or_,
            (Q(generic_product__categories__name__icontains = \
                cate) for cate in cates)
        )
    except Exception as e:
        print(e)
        return None
    return query

def make_query_by_name(name_query):
    if not name_query:
        return None
    return Q(name__icontains=name_query)

class GenericProductVewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GenericProduct.objects.all()
    serializer_class = GenericProductSerializer

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AttributeClassViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = AttributeClass.objects.all()
    serializer_class = AttributeClassSerializer
    
class SpecificProductViewSet(viewsets.ViewSet,
                            generics.ListAPIView, 
                            generics.RetrieveAPIView):
    queryset = SpecificProduct.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpecificProductDetailSerializer
        return SpecificProductSerializer
    
    def get_object(self):
        sleep(0.5)
        return super().get_object()
    
    def get_queryset(self):
        sleep(1)
        products = super().get_queryset()
        if self.action == 'list':

            cate_query = make_query_by_category(
                self.request.query_params.get('category')
            )
            attr_query = make_query_by_attr(
                self.request.query_params.get('attribute')
            )
            price_query = make_query_by_price_range(
                self.request.query_params.get('range') 
            )
            name_query = make_query_by_name(
                self.request.query_params.get('q')
            )

            try:
                query_list = [name_query, cate_query, attr_query, price_query]
                query = reduce(operator.and_, (q for q in query_list if q is not None))
            except TypeError:
                query=None

            if query:
                products = products.filter(
                    query
                ).distinct()


        return products
