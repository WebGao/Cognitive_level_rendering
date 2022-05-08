from django.urls import path
from .logistics import main

urlpatterns = [
    path('logistics/train', main.train_server),
]
