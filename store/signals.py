from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils.text import slugify

from accounts.models import CustomUser
from api import settings
from store.models import Cart, Product


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

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_cart(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(user=instance)