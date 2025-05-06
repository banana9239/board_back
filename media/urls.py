from django.urls import path
from media.views import getURL, uploadImage, getImages

urlpatterns = [
    path("get-url", getURL.as_view()),
    path("<int:postPk>/imageUpload", uploadImage.as_view()),
    path("<int:postPk>/getImages", getImages.as_view()),
]
