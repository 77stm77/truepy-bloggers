"""truepy_bloggers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as core_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.homepage.as_view(), name="homepage"),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout_view, name="logout"),
    path('login/', user_views.login_view, name="login"),
    path('post_publish/', core_views.post_publish, name="create"),
	path('must_authenticate/', user_views.must_authenticate_view, name="must_authenticate"),
    path('post/<int:id>/', core_views.post_view, name="post"),
    path('edit/<int:id>/', core_views.edit_post, name="edit"),
    path('delete/<int:id>/', core_views.delete_post, name="delete"),
    path('my_blog/<int:id>/', user_views.my_blog, name="my_blog")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
