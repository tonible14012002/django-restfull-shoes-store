from django.urls import path, include
from rest_framework import routers
from . import views
from django.http import HttpResponse

router = routers.DefaultRouter()
router.register('items', views.CartViewSet, basename='cart')

app_name = 'cart'
urlpatterns = [
    path('', include(router.urls))
]