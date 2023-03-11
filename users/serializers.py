from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
# TODO Здесь нам придется переопределить сериалайзер, который использует djoser
# TODO для создания пользователя из за того, что у нас имеются нестандартные поля


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    pass


class CurrentUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=60)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    # phone = PhoneNumberField(null=False, blank=False, unique=True, verbose_name='Телефон')
    last_login = serializers.DateTimeField(read_only=True)
    role = serializers.CharField()
