from django.urls import path
from .views import *

urlpatterns = [
    path('', AllPostsList.as_view(), name='all_posts'),
    path('news', NewsList.as_view(), name='all_news'),
    path('articles', ArticleList.as_view(), name='all_articles'),
    path('posts/<int:pk>', PostView.as_view(), name='post'),
    path('news/<int:pk>', NewsView.as_view(), name='news'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),
    # path('posts/create', create_post, name='post_create'),
    path('news/create', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('search', SearchPostList.as_view(), name='search'),
]