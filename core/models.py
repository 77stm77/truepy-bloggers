
from django.db import models
from django.urls import reverse
from users.models import Account


class Post(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    lk_count = models.PositiveIntegerField(default=0)
    dislk_count = models.PositiveIntegerField(default=0)
    user_like_react = models.ManyToManyField(Account, blank=True, related_name="user_like_react")
    user_dislike_react = models.ManyToManyField(Account, blank=True, related_name="user_dislike_react")    
    
    class Meta:
        ordering = ["-date_time"]

    def get_absolute_url(self):
        return reverse("post", kwargs={"id": self.id})

    def __str__(self):
        return self.name



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='comments_of_authors')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

class Subscribed(models.Model):
    subs = models.ManyToManyField(Account, null=True)

    def __str__(self):
        return self
