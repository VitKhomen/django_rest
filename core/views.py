from rest_framework import viewsets, filters, pagination, generics, \
    permissions, views
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from taggit.models import Tag

from .serializers import PostSerializer, TagSerializer, ContactSerializer, \
    RegisterSerializer, UserSerializer
from .models import Post


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['created_at', 'title']
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(
                f'От {name} | {subject}',
                message,
                from_email,
                ['vital210890@gmail.com']
            )
            return Response({"success": "Sent"})
        return Response(serializer.errors, status=400)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(
                user, context=self.get_serializer_context()).data,
            'message': 'User created successfully'
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(
                request.user,
                context=self.get_serializer_context()
            ).data,
        })
