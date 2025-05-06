from typing import Any
from django.db import models
from common.models import CommonModel
import bcrypt
from config.settings import P_SORT

class Post(CommonModel):
    class sortationChoices(models.TextChoices):
        notice = ('공지', 'NOTICE')
        free = ('자유', 'FREE')

    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    board = models.ForeignKey(
        'board.Board',
        on_delete=models.CASCADE,
    )
    sortation = models.CharField(max_length=20,choices=sortationChoices.choices)
    is_deleted = models.BooleanField(default=False)
    secret_code = models.CharField(max_length=60, blank=True, null=True, default="")

    def __str__(self):
        return self.title
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        self.is_deleted = True
        self.save()
    
    def like_count(post):
        return post.postlike_set.count()
        
    def browsing_count(post):
        return post.browsing_set.count()
    
    def set_secret_code(self, raw_code: str):
        hashed = bcrypt.hashpw((raw_code+P_SORT).encode('utf-8'), bcrypt.gensalt())
        self.secret_code = hashed.decode('utf-8')

    def check_secret_code(self, raw_code: str) -> bool:
        return bcrypt.checkpw((raw_code+P_SORT).encode('utf-8'), self.secret_code.encode('utf-8'))

class PostComment(CommonModel):
    content = models.TextField()
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'Post',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        self.is_deleted = True
        self.save()
    
class CommenReply(CommonModel):
    content = models.TextField()
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        'PostComment',
        on_delete=models.CASCADE,
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.content
    
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        self.is_deleted = True
        self.save()
    

class Browsing(CommonModel):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_browsing')
        ]
    
    def __str__(self) -> str:
        return f'{self.user} - {str(self.post)[:5]}...'

class PostLike(CommonModel):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_postlike')
        ]