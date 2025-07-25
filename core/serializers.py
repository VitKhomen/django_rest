from .models import Comment
from rest_framework import serializers
from django.utils.html import strip_tags

from taggit.models import Tag

from .models import Post, Comment, CustomUser


class PostSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    author = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all())

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
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "avatar",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password2": "Пароли не совпадают"})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'avatar', 'date_joined',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "author", "author_avatar", "text", "created_date")
        read_only_fields = ("author", "author_avatar", "created_date")

    def get_author(self, obj):
        return obj.author.username

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        if obj.author.avatar:
            return request.build_absolute_uri(obj.author.avatar.url)
        return None
