from django.contrib import admin
from core.models import Post, Comment, Subscribed, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscribed)
admin.site.register(Like)
