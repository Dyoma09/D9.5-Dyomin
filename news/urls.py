from django.urls import path
from .views import  *

handler403 = 'news.views.error_403'

urlpatterns = [
    path('news/', ListNews.as_view(), name='news_list'),
    path('news/search/', ListNewsSearch.as_view(), name='news_search'),
    path('news/<int:pk>', DetailNews.as_view(), name='news'),
    path('news/create', CreateNews.as_view(), name='news_create'),
    path('news/<int:pk>/update', UpdateNews.as_view(), name='news_update'),
    path('news/<int:pk>/delete', DeleteNews.as_view(), name='news_delete'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('news/upgrade/', upgrade_me, name='upgrade'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]