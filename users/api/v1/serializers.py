from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class DepositSerializer(serializers.Serializer):
    deposit = serializers.IntegerField()

    def validate_deposit(self, value):
        """
        check for multiple of 5 or not else raise exception
        """
        if value % 5 != 0:
            raise serializers.ValidationError("deposit is not multiple of 5")
        elif value not in [5, 10, 20, 50, 100]:
            raise serializers.ValidationError(
                "The deposit amount has to be one of 5, 10, 20, 50, or 100 cent coins"
            )
        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["is_buyer", "is_seller"]


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()


class SignupSerializer(serializers.ModelSerializer):
    is_buyer = serializers.BooleanField(write_only=True, default=False)
    is_seller = serializers.BooleanField(write_only=True, default=False)
    deposit = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "is_buyer",
            "is_seller",
            "deposit",
        )
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }

    def validate_deposit(self, value):
        """
        check for multiple of 5 or not else raise exception
        """
        if value % 5 != 0:
            raise serializers.ValidationError("deposit is not multiple of 5")
        elif value not in [5, 10, 20, 50, 100]:
            raise serializers.ValidationError(
                "The deposit amount has to be one of 5, 10, 20, 50, or 100 cent coins"
            )
        return value

    def create(self, validated_data):
        # get profile props
        is_buyer = validated_data.get("is_buyer")
        is_seller = validated_data.get("is_seller")
        deposit = validated_data.get("deposit")
        # handle user creation
        user = User(
            username=validated_data.get("username"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        # get user profile
        profile = Profile.objects.get(user=user)
        # handle profile fields and save
        profile.is_buyer = is_buyer
        profile.is_seller = is_seller
        profile.deposit = deposit
        profile.save()
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()
