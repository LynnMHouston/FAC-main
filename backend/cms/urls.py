from django.urls import path
from . import views

urlpatterns = [
    # home page
    path("", views.home.as_view(), name="posts"),
    # route for posts
    path("<slug:slug>/", views.postdetail.as_view(), name="post_detail"),
]