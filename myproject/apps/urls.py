from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("", views.index, name="index"),
    path("counter", views.counter, name="counter"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("post", views.post, name="post"),
    path("article/<str:pk>", views.article, name="article"),
    path("delete/<str:pk>", views.del_article, name="delete"),
    path("predict", views.predict, name="predict"),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
