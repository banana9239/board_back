from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Post, PostComment, PostLike, CommenReply, Browsing
from user.serializers import UserSerializer
from board.models import Board

class PostSerializer(ModelSerializer):
    
    like_count = SerializerMethodField()
    browsing_count = SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_like_count(self, post):
        return post.like_count()
    
    def get_browsing_count(self, post):
        return post.browsing_count()
    
    def create(self, validated_data):
        secret_code = validated_data.pop('secret_code', None)
        post = super().create(validated_data)
        if secret_code:
            post.set_secret_code(secret_code)
            post.save()
        return post
    
class PostListSerializer(ModelSerializer):

    comment_count = SerializerMethodField()
    like_count = SerializerMethodField()
    browsing_count = SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "like_count",
            "browsing_count",
            "comment_count",
            "board",
            "sortation",
            "created_at",
            "updated_at",
        ]

    def get_like_count(self, post):
        return post.postlike_set.count()

    def get_browsing_count(self, post):
        return post.browsing_set.count()
    
    def get_comment_count(self, post):
        return post.comments.filter(is_deleted=False).count()

class PostCommentSerializer(ModelSerializer):

    author = UserSerializer(read_only=True)
    replies = SerializerMethodField()
    
    class Meta:
        model = PostComment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
            'replies',
        ]

    def get_replies(self, comment):
        replies = comment.commenreply_set.filter(is_deleted=False)
        serializer = CommentReplySerializer(replies, many=True)
        return serializer.data

class PostDetailSerializer(ModelSerializer):

    like_count = SerializerMethodField()
    browsing_count = SerializerMethodField()
    author = UserSerializer(read_only=True)
    comments = SerializerMethodField()
    board_name = SerializerMethodField()
    comment_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_like_count(self, post):
        return post.like_count()
    
    def get_browsing_count(self, post):
        return post.browsing_count()
    
    def get_comments(self, post):
        comments = post.comments.filter(is_deleted=False)
        serializer = PostCommentSerializer(comments, many=True)

    def get_board_name(self, post):
        return post.board.board_name
    
    def get_comment_count(self, post):
        return post.comments.filter(is_deleted=False).count()

    

class CommentReplySerializer(ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = CommenReply
        fields = [
            'id',
            'content',
            'author',
            'created_at',
        ]

