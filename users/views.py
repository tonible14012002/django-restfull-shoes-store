from copyreg import constructor
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import (viewsets, generics)
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailSerializer, UserSerializer
# Create your views here.

User = get_user_model()

class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        else :
            return UserSerializer

    def get_queryset(self):
        users = User.objects.filter(is_active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            users = users.filter(
                Q(email__icontains=q)|
                Q(first_name__icontains=q)|
                Q(last_name__icontains=q)
            )
        return users
    