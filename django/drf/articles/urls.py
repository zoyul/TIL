from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),

    path('<int:pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:article_pk>/comments_list/', views.comments_list, name='comments_list'),
    path('<int:comment_pk>/comment_update/', views.comment_update, name='comment_update'),
]
