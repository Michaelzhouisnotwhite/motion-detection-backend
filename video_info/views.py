from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from video_info.models import VideoInfo

from video_info.serializers import VideoInfoSerializer


# Create your views here.
class VideoInfoList(APIView):

    def get(self, request, format=None):
        info = VideoInfo.objects.all()
        res = VideoInfoSerializer(info, many=True)
        return Response(res.data)


class VideoInfoDetail(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return VideoInfo.objects.get(pk=pk)
        except VideoInfo.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        if not VideoInfo.objects.filter(title = request.data['title']).exists():
            VideoInfo.objects.filter(pk=pk).update(title=request.data['title'])
            return Response()
        return Response({"message":'名称重复'}, status=status.HTTP_406_NOT_ACCEPTABLE)
