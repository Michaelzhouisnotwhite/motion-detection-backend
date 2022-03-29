import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import StreamingHttpResponse
import cv2 as cv
from dashboard.settings import MEDIA_ROOT
import time
# Create your views here.


def get_display(cap: cv.VideoCapture):
    frame_counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            flag, frame = cv.imencode('.jpeg', frame)
            time.sleep(0.05) 
            frame_counter += 1
            if frame_counter == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                frame_counter = 0
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            if flag:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@api_view(['GET', 'POST'])
def video_streamer(request):

    cap = cv.VideoCapture(os.path.join(MEDIA_ROOT, 'test_video.mp4'))
    # get_display(cap)

    return StreamingHttpResponse(get_display(cap), content_type='multipart/x-mixed-replace; boundary=frame')
