from django.urls import path
from . import views

urlpatterns = [
    path("", views.Posts.as_view()),
    path("board/<int:pk>", views.PostList.as_view()),
    path("<int:pk>", views.PostDetail.as_view()),
    path("<int:pk>/like", views.PostLikeDo.as_view()),
    path("<int:pk>/comment", views.PostComments.as_view()),
    path("comment/<int:pk>", views.PostCommentDetail.as_view()),
    path("comment/<int:pk>/reply", views.CommentReplies.as_view()),
    path("reply/<int:pk>", views.CommentReplyDetail.as_view()),
]