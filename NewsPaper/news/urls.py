from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(AllPostsList.as_view()), name='all_posts'),
    path('news', cache_page(60*5)(NewsList.as_view()), name='all_news'),
    path('articles', cache_page(60*5)(ArticleList.as_view()), name='all_articles'),
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
    path('subscribe/', subscribe, name='subscribe'),
    # path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    # path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('become_an_author/', become_an_author, name='become_an_author'),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout_user, name='logout'),
]