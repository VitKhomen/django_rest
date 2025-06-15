from .models import Comment
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.html import strip_tags

from taggit.models import Tag

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ("id", "title", "slug", "description",
                  "content", "image", "created_at", "author", "tags")
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_description(self, obj):
        return strip_tags(obj.description)[:300] + "..."

    def get_content(self, obj):
        return strip_tags(obj.content)


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ('name', 'post_count')
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(
        slug_field="slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "text", "created_date")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
