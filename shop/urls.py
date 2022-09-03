
from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register('product-list', views.SpecificProductViewSet)
router.register('categories', views.CategoryViewSet)
router.register('attribute-class', views.AttributeClassViewSet)


app_name='shop'
urlpatterns = [
    path('', include(router.urls))
]