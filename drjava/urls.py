from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("ordered", views.ordered, name="ordered"),
    path("interact", views.interact, name="interact"),
]

