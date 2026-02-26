from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from store.models import Product


@receiver(pre_save, sender=Product)
def generate_slug(sender,instance,**kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        slug = base_slug
        counter = 1

        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug