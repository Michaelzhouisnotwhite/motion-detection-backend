from rest_framework import serializers
from video_info.models import VideoInfo


class VideoInfoSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = VideoInfo
        fields = ['id', 'title', 'size', 'duration', 'created', 'falling']