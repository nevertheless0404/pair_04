from django.urls import path
from . import views

app_name = "reviews"
urlpatterns = [
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("detail/<int:pk>", views.detail, name="detail"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("update/<int:pk>", views.update, name="update"),
    path("<int:reviews_pk>/comments", views.comment_create, name="comment_create"),
    path(
        "<int:reviews_pk>/comments/<int:comment_pk>/update",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:reviews_pk>/comments/<int:comment_pk>/delete",
        views.comment_delete,
        name="comment_delete",
    ),
]
