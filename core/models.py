from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from unidecode import unidecode


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.png', blank=True, null=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='post_images/',
                              default='post_images/default.png')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title))[:90]
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text
