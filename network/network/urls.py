# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path('accounts/login/', views.login_view),  
    path("all_posts", views.all_posts, name="all_posts"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("toggle_follow/<int:user_id>", views.toggle_follow, name="toggle_follow"),
    path("following", views.following, name="following"),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
]