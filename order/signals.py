from atexit import register
from operator import ipow
from django.dispatch import receiver
from django.db.models.signals import (
    post_save
)
from order.models import (
    Order, 
    OrderItem
)

