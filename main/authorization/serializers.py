from rest_framework import serializers
from .models import User
from django.conf import settings


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
        print('зашел в криет')
        confirm_password = validated_data.pop("confirm_password")
        password = validated_data.get("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_email(self, value):
        print('валидация почты')
        if User.objects.filter(email=value).exists():
            print('пароль существует')
            print(User.objects.filter(email=value))
            raise serializers.ValidationError("Email already exists.")
        print('такого пароля нету')
        return value

    def validate_password(self, value):
        print('валидация пароля')
        if len(value) < getattr(settings, "PASSWORD_MIN_LENGTH", 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long."
                % getattr(settings, "PASSWORD_MIN_LENGTH", 8)
            )
        return value

    def validate_confirm_password(self, value):
        print('валидация 2 пароля')
        password = self.initial_data.get("password")
        if password != value:
            raise serializers.ValidationError("Password incorrect.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio']