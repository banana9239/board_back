from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "nickname",
        )

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "nickname",
            "email",
            "is_active",
            "birth_date",
            "date_joined",
        )