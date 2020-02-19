from django.db import models
from django.urls import reverse
from users.models import Account


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    lk_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date_time"]

    def get_absolute_url(self):
        return reverse("post", kwargs={"id": self.id})

    def __str__(self):
        return self.name

class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='lk_author')
    post = models.ManyToManyField(Post, blank=True, related_name="lk_post")

    def __str__(self):
        return self.id


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='comments_of_authors')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.author.username

class Subscribed(models.Model):
    subs = models.ManyToManyField(Account, null=True)

    def __str__(self):
        return self
