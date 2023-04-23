from django.urls import path
from .views import PostsList, NewsList, PostView, NewsView

urlpatterns = [
    path('news', NewsList.as_view()),
    path('posts', PostsList.as_view()),
    path('posts/<int:pk>', PostView.as_view()),
    path('news/<int:pk>', NewsView.as_view()),
]