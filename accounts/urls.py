from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("", views.login, name="login"),
    path("<int:pk>/profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("delete/", views.delete, name="delete"),
]
