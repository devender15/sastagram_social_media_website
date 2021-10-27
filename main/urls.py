from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('uploading', views.add_post, name="add_post"),
    path('<str:username>', views.profile, name="profile"),
    path('edit/', views.edit_profile, name="edit"),
    path('follow/', views.follow, name="follow")
]