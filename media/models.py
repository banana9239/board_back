from django.db import models
from common.models import CommonModel

class Photo(CommonModel):
    image = models.URLField()
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.author.username
    

class Video(CommonModel):
    video = models.URLField()
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)