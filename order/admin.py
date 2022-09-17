from msilib.schema import SelfReg
from django.contrib import admin
from .models import (
    Order,
    OrderItem,   
) 
# Register your models here.

class OrderItemInline(admin.StackedInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'city', 'address', 'status', 'paid')
    inlines = (OrderItemInline,)
    readonly_fields = list_display
    list_filter = ('status', 'paid', 'city', 'created_at','updated_at')

