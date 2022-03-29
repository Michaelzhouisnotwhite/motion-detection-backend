from django.urls import path
from video_streamer import views


urlpatterns = [
    path('display', views.video_streamer)
]