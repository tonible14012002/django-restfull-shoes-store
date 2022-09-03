from asyncio import SendfileNotAvailableError
from math import prod
from ssl import create_default_context
from time import process_time_ns
from django.db.models.signals import (
    m2m_changed,
    post_save,
    pre_save,
    pre_delete
)
from django.dispatch import receiver
from .models import ProductOption, SpecificProduct
import json


# handle attribute query string changed after attributes changed
@receiver(m2m_changed, sender=SpecificProduct.attributes.through)
def attributes_changed(sender, instance, **kwargs):
    attrs = json.loads(instance.attributes_str)
    attrs['attributes'] = ','.join([attr.value for attr in instance.attributes.all()])
    instance.attributes_str = json.dumps(attrs)
    instance.save()

@receiver([post_save, pre_delete], sender=ProductOption)
def option_saved(sender, instance, **kwrags):
    product = instance.specific_product
    attrs = json.loads(product.attributes_str)
    sizes = ','.join([f's{option.size.size}' for option in product.product_options.all()])
    attrs['sizes'] = sizes
    product.attributes_str = json.dumps(attrs)
    product.save()
    print(product.attributes_str)

@receiver(pre_save, sender=SpecificProduct)
def Product_saved(sender, instance, **kwargs):
    if instance.color:        
        attrs = json.loads(instance.attributes_str)
        attrs['color'] = instance.color.name
        instance.attributes_str = json.dumps(attrs)