from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import SpecificProduct

@receiver(m2m_changed, sender=SpecificProduct.attributes.through)
def attributes_changed(sender, instance, **kwargs):
    print(instance)
    instance.attributes_str = \
        ','.join([attr.name for attr in instance.attributes.all()])
    instance.save()