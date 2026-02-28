import os

from django.db import models
from django.contrib.auth.models import AbstractUser

from api import settings

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True,default=20)



def upload_path(instance,filename):
    return os.path.join('images','avatars',str(instance.user.id),filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    bio = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=upload_path,blank=True,null=True)