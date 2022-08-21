from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, 
    PermissionsMixin
    ) 
from django.utils.translation import gettext_lazy as _
# Create our models here.

class UserManager(BaseUserManager):
    """_summary_
    Custom user model manager where email is the unique identifier
    for authenticaton instead of usernames/
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save user with given email and password
        """
        if not email:
            raise ValueError(('the Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField('email address',max_length=320, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    avatar = models.ImageField(upload_to='user/avatar/%y/%m/%d',
                               null=True, blank=True)

    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def __str__(self):
        return self.email
    