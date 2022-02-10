from rest_framework import exceptions
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
    def get_object(pk) -> VideoInfo:
        try:
            return VideoInfo.objects.get(pk=pk)
        except VideoInfo.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk, format=None):
        if not VideoInfo.objects.filter(title=request.data['title']).exclude(pk=pk).exists():
            VideoInfo.objects.filter(pk=pk).update(title=request.data['title'])
            return Response()
        return Response({"message": '名称重复'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk=pk)
        obj.delete()
        return Response({"message": '删除成功', "id": pk}, status=status.HTTP_301_MOVED_PERMANENTLY)
