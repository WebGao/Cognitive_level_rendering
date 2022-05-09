from django.urls import path
from .logistics import main

urlpatterns = [
    path('logistics/<int:topic>/train', main.train_server),
    path('logistics/<int:topic>/predict', main.predict_server),
    path('logistics/<int:topic>/record', main.record_server),
    path('logistics/<int:topic>/recommend', main.recommend_server),
]
