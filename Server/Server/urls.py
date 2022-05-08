from django.urls import path
from .logistics import main

urlpatterns = [
    path('logistics/train', main.train_server),
    path('logistics/predict', main.predict_server),
    path('logistics/record', main.record_server),
]
