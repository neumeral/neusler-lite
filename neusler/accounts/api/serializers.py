from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import User


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"), username=username, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials")
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_active:
                msg = _("Account not active")
                raise serializers.ValidationError(msg, code="not active")

        else:
            msg = _('Must include "username" and "password"')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "display_name",
            "city",
            "country_code",
            "avatar",
        ]


class SignupInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        if email and username:
            if User.objects.filter(email__iexact=email).exists():
                msg = _("Email already registered")
                raise serializers.ValidationError(msg, code="user_exists")
            elif User.objects.filter(username__iexact=username).exists():
                msg = _("Username already exists")
                raise serializers.ValidationError(msg, code="user_exists")
        return attrs

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
