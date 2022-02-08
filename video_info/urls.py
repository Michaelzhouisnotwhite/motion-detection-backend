from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from video_info import views

urlpatterns = [
    path('video_info/', views.VideoInfoList.as_view()),
    path('video_info/<int:pk>/', views.VideoInfoDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)