from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Create serializer class for User model
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'password'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Retrieve serializer class for User model
    """
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'avatar'
        ]
