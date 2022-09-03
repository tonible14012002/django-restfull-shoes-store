from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register('all', views.UserViewSet)

app_name='users'
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view()),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view())
]