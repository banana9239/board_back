from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db import transaction, IntegrityError
from . import serializers
from board.models import Board
from .models import Post, Browsing, PostLike, PostComment, CommenReply


class Posts(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        board_pk = request.data.get("data").get("board",None)
        
        if not board_pk:
            raise ParseError("Board is required.")
        try:
            board = Board.objects.get(pk=board_pk)
        except Board.DoesNotExist:
            raise ParseError("Board does not exist.")

        serializer = serializers.PostSerializer(data=request.data.get("data"))
        if serializer.is_valid():
            with transaction.atomic():
                new_post = serializer.save(author=request.user)
                return Response(serializers.PostSerializer(new_post).data)
        else:
            return Response(serializer.errors)
        
class PostList(APIView):
        
    def get(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
            posts = board.post_set.filter(is_deleted=False)
            serializer = serializers.PostListSerializer(posts, many=True)
            return Response(serializer.data)
        except Board.DoesNotExist:
            raise ParseError("Board does not exist.")
    
class PostDetail(APIView):
        
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk, secret_code):
        try:
            post = Post.objects.get(pk=pk)
            if secret_code:
                if post.check_secret_code(secret_code):
                    return post
                else:
                    raise ParseError("Invalid secret code")
            return post
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_object(pk, request.data.get("secret_code"))
        serializer = serializers.PostDetailSerializer(post)

        if request.user.is_authenticated:
            try:
                with transaction.atomic():
                    browsing = Browsing.objects.create(user=request.user, post=post)
            except IntegrityError:
                pass
            return Response(serializer.data)
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            raise PermissionDenied
        serializer = serializers.PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                post = serializer.save()
            return Response(serializers.PostDetailSerializer(post).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, is_deleted=False)
            if post.author != request.user:
                raise PermissionDenied
            post.delete()
            return Response({"message": "Post deleted."})
        except Post.DoesNotExist:
            return NotFound
        
    
class PostLikeDo(APIView):
        
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        post = self.get_object(pk)
        try:
            like = PostLike.objects.get(user=request.user, post=post)
            return Response(status=HTTP_200_OK)
        except PostLike.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
            

    def post(self, request, pk):
        post = self.get_object(pk)
        try:
            with transaction.atomic():
                post_like = PostLike.objects.create(user=request.user, post=post)
        except IntegrityError:
            pass
        return Response({"message": "Post liked."})
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        try:
            post_like = PostLike.objects.get(user=request.user, post=post)
            post_like.delete()
        except PostLike.DoesNotExist:
            ParseError("Already unliked.")
        return Response({"message": "Post unliked."})
        

class PostComments(APIView):
        
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,pk):
        post = Post.objects.get(pk=pk)
        comments = post.comments.filter(is_deleted=False)
        serializer = serializers.PostCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = serializers.PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save(author=request.user, post=post)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
class PostCommentDetail(APIView):
            
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return PostComment.objects.get(pk=pk)
        except PostComment.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = serializers.PostCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if comment.author != request.user:
            raise PermissionDenied
        serializer = serializers.PostCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                comment = serializer.save()
            return Response(serializers.PostCommentSerializer(comment).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        comment = self.get_object(pk)
        if comment.author != request.user:
            raise PermissionDenied
        comment.delete()
        return Response({"message": "Comment deleted."})
        
class CommentReplies(APIView):
        
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        comment = PostComment.objects.get(pk=pk)
        serializer = serializers.CommentReplySerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save(author=request.user, comment=comment)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
class CommentReplyDetail(APIView):
                
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return CommenReply.objects.get(pk=pk)
        except CommenReply.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        reply = self.get_object(pk)
        serializer = serializers.CommentReplySerializer(reply)
        return Response(serializer.data)

    def put(self, request, pk):
        reply = self.get_object(pk)
        if reply.author != request.user:
            raise PermissionDenied
        serializer = serializers.CommentReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                reply = serializer.save()
            return Response(serializers.CommentReplySerializer(reply).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        reply = self.get_object(pk)
        if reply.author != request.user:
            raise PermissionDenied
        reply.delete()
        return Response({"message": "Reply deleted."})