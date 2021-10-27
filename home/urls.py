from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('postComment/', views.post_comments, name="posting_comment")
]