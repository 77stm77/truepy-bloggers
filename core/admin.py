from django.contrib import admin
from core.models import Post, Comment, Subscribed

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Subscribed)
