from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    '''
    BaseModel class including base fields
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=45, blank=True)
    last_name = models.CharField(max_length=45, blank=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
