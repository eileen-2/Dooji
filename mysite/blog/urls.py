from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='blog_detail'),
    path('create/', views.PostCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='blog_delete'),
    path('<int:pk>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('blog/<int:pk>/likes/', views.LikeCreateView.as_view(), name='like_create'),
]