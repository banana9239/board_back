from django.urls import path
from . import views

urlpatterns = [
    path("largeCategories", views.LargeCategories.as_view()),
    path("mediumCategories", views.MediumCategories.as_view()),
    path("smallCategories", views.SmallCategories.as_view()),
    path("largeCategoryList", views.LargeCategoryList.as_view()),
    path("<int:pk>/mediumCategoryList", views.MediumCategoryList.as_view()),
    path("<int:pk>/smallCategoryList", views.SmallCategoryList.as_view()),
    path("largeCategory/<int:pk>", views.LargeCategoryDetail.as_view()),
    path("mediumCategory/<int:pk>", views.MediumCategoryDetail.as_view()),
    path("smallCategory/<int:pk>", views.SmallCategoryDetail.as_view()),
    path('boards', views.Boards.as_view()),
    path('<int:pk>/boards', views.BoardList.as_view()),
    path("<int:pk>", views.BoardDetail.as_view()),
]

