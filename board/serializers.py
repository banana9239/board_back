from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import LargeCategory, MediumCategory, SmallCategory, Board

class SmallCategorySerializer(ModelSerializer):
    class Meta:
        model = SmallCategory
        fields = '__all__'

class MediumCategorySerializer(ModelSerializer):
    class Meta:
        model = MediumCategory
        fields = '__all__'

class LargeCategorySerializer(ModelSerializer):
    class Meta:
        model = LargeCategory
        fields = '__all__'

class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class BoardDetailSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

    # Board에 연결되어 있는 Post의 개수
    post_count = SerializerMethodField()
    
    def get_post_count(self, obj):
        return obj.post_set.count()
    