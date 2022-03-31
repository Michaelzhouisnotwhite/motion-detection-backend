import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, StreamingHttpResponse
import cv2 as cv
from dashboard.settings import MEDIA_ROOT
import time
from dashboard.settings import BASE_DIR

from video_streamer.obj_detection import ObjDetection
# Create your views here.

CONF = 0.7
IS_DETECTED = False
CAMON = False
DURATION = 5


def get_display(cap: cv.VideoCapture):
    global CONF
    global IS_DETECTED, CAMON,DURATION
    frame_counter = 0
    obj_model = ObjDetection(os.path.join(BASE_DIR, "video_streamer/weights/best.pt"), [480, 480])

    while cap.isOpened():
        if CAMON:
            ret, frame = cap.read()
            if ret:
                frame_counter += 1
                # print(IS_DETECTED, CONF)
                if IS_DETECTED:
                    objs = obj_model(frame, CONF, 0.5)

                    saved_img = obj_model.draw(frame.copy(), objs)
                    if objs is not None and objs != [] and frame_counter % int(DURATION) == 0:
                        cv.imwrite(os.path.join(MEDIA_ROOT, 'catched.png'), saved_img)
                else:
                    saved_img = frame
                flag, output = cv.imencode('.jpeg', saved_img)

                if frame_counter == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                    frame_counter = 0
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                if flag:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + output.tobytes() + b'\r\n')



@api_view(['GET'])
def catched_picture(request):
    try:
        image_data = open(os.path.join(MEDIA_ROOT, 'catched.png'), "rb").read()
    except FileNotFoundError:
        return Response(status=404)
    return HttpResponse(image_data, content_type="image/png")


@api_view(['GET', 'POST'])
def video_streamer(request):
    global CAMON
    if request.method == 'GET':
        cap = cv.VideoCapture(os.path.join(MEDIA_ROOT, 'my_test02.mp4'))
    # get_display(cap)
    if CAMON:
        return StreamingHttpResponse(get_display(cap), content_type='multipart/x-mixed-replace; boundary=frame')
    return Response(status=200)


@api_view(['POST'])
def detect_settings(request):
    global IS_DETECTED, CONF, CAMON
    data = request.data
    if data['isDetecting']:
        IS_DETECTED = True
    else:
        IS_DETECTED = False

    if data['isCamOn']:
        CAMON = True
    else:
        CAMON = False
    # if data.is
    # print(request.data)
    return Response()


@api_view(['POST'])
def warning_settings(request):
    global CONF,DURATION
    data = request.data
    CONF = data['filter']
    DURATION = data['duration'],
    if isinstance(DURATION, tuple):
        DURATION = DURATION[0]
    return Response()
