import mimetypes
import re
import os
from wsgiref.util import FileWrapper
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse

def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
  with open(file_name, "rb") as f:
    f.seek(offset, os.SEEK_SET)
    remaining = length
    while True:
      bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
      data = f.read(bytes_length)
      if not data:
        break
      if remaining:
        remaining -= len(data)
      yield data

@api_view(['GET', 'POST'])
def stream_video(request, path):
  """将视频文件以流媒体的方式响应"""
  range_header = request.META.get('HTTP_RANGE', '').strip()
  range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
  range_match = range_re.match(range_header)
  
  path = os.path.join(settings.BASE_DIR / 'media', path)
  
  size = os.path.getsize(path)
  content_type, encoding = mimetypes.guess_type(path)
  content_type = content_type or 'application/octet-stream'
  if range_match:
    first_byte, last_byte = range_match.groups()
    first_byte = int(first_byte) if first_byte else 0
    last_byte = first_byte + 1024 * 1024 * 8    # 8M 每片,响应体最大体积
    if last_byte >= size:
      last_byte = size - 1
    length = last_byte - first_byte + 1
    resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206, content_type=content_type)
    resp['Content-Length'] = str(length)
    resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
  else:
    # 不是以视频流方式的获取时，以生成器方式返回整个文件，节省内存
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Content-Length'] = str(size)
  resp['Accept-Ranges'] = 'bytes'
  return resp