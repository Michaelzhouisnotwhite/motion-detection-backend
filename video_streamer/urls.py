from django.urls import path
from video_streamer import views

urlpatterns = [
    path('display', views.video_streamer),
    path('dis-settings', views.set_detect_settings),
    path('warning-settings', views.set_warning_settings),
    path('caught', views.get_caught_picture),
    path('recover_settings', views.recover_settings),
    path('clear_cache', views.clear_cache)
]
