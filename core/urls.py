from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagDetailView, TagView, AsideView, \
    FeedBackView, RegisterView, ProfileView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagView.as_view(), name='tag-list'),
    path('aside/', AsideView.as_view(), name='aside-list'),
    path('tags/<slug:tag_slug>/', TagDetailView.as_view()),
    path('feedback/', FeedBackView.as_view(), name='feedback'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
