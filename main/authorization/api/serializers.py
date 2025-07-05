from rest_framework import serializers
from ..models import User, Subscription
from django.conf import settings
import requests
from ..tasks import upload_avatar


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password")
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password")
        password = validated_data.get("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Такая почта уже зарегестрирована ")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, "PASSWORD_MIN_LENGTH", 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long."
                % getattr(settings, "PASSWORD_MIN_LENGTH", 8)
            )
        return value

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")
        if password != value:
            raise serializers.ValidationError("Неправильный пароль")
        return value

    def validate_username(self, value):
        if len(value) > 40:
            raise serializers.ValidationError("Ник не может превышать 40 символов")
        if len(value.split()) != 1:
            raise serializers.ValidationError("В нике не может быть пробелов")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким ником уже существует")
        return value


class UserSerializer(serializers.ModelSerializer):
    photo = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'mark','photo', 'username', 'bio', 'avatar']

    def update(self, instance, validated_data):
        if validated_data.get('photo'):
            photo = validated_data.pop('photo')
            upload_avatar.delay(photo.read(), instance.id)
        return super().update(instance, validated_data)

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ['user']

    def create(self, validated_data):
        validated_data['subscriber'] = self.context['request'].user
        return super().create(validated_data)