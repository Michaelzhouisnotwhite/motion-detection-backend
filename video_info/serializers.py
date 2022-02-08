from rest_framework import serializers
from video_info.models import VideoInfo
from django.utils import timezone

def get_default_title():
    now_time = timezone.localtime(timezone.now())
    return now_time.strftime("%Y%m%d_%H%M%S")

class VideoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInfo
        fields = ['id', 'title', 'size', 'duration', 'created', 'falling']