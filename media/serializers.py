from rest_framework.serializers import ModelSerializer, SerializerMethodField
from user.serializers import UserSerializer
from post.serializers import PostSerializer
from .models import Photo

class PhotoSerializer(ModelSerializer):
    
    class Meta:
        model = Photo
        fields = '__all__'
