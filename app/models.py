from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('first name', max_length=45, blank=True)
    last_name = models.CharField('last name', max_length=45, blank=True)
    is_active = models.BooleanField('active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
