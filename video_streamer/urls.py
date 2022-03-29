from django.urls import path
from video_streamer import views


urlpatterns = [
    path('display', views.video_streamer),
    path('dis-settings', views.detect_settings),
    path('warning-settings', views.warning_settings),
    path('catched', views.catched_picture)
]