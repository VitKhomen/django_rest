from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, \
    FeedBackView, RegisterView, ProfileView, CommentView, LogoutView, \
    CommentDetaliView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagView.as_view(), name='tag-list'),
    path('aside/', AsideView.as_view(), name='aside-list'),
    path('tags/<slug:tag_slug>/', TagDetailView.as_view()),
    path('contacts/', FeedBackView.as_view(), name='feedback'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('comments/id/<int:pk>/', CommentDetaliView.as_view()),
    path('comments/post/<slug:post_slug>/', CommentView.as_view()),
]
