from django.db import models
from django.urls import reverse
from users.models import Account


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    img_1 = models.ImageField(default="post_images/default.png", upload_to="post_images")
    img_2 = models.ImageField(default="post_images/default.png", upload_to="post_images")
    img_3 = models.ImageField(default="post_images/default.png", upload_to="post_images")
    img_4 = models.ImageField(default="post_images/default.png", upload_to="post_images")
    img_5 = models.ImageField(default="post_images/default.png", upload_to="post_images")

    def get_absolute_url(self):
        return reverse("post", kwargs={"id": self.id})

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='comments_of_authors')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.author.username
