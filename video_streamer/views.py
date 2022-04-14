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
CAM_ON = False
DURATION = 5
caught_pic_path = f'{MEDIA_ROOT}/caught.jpeg'

obj_model = ObjDetection(os.path.join(BASE_DIR, "video_streamer/weights/best.pt"), [480, 480])

MESSAGE_SENT = 0


def get_video(cap: cv.VideoCapture):
    global CONF
    global IS_DETECTED, CAM_ON, DURATION, caught_pic_path, obj_model
    frame_counter = 0

    while cap.isOpened():
        if CAM_ON:
            ret, frame = cap.read()
            if ret:
                frame_counter += 1
                if IS_DETECTED:
                    objs = obj_model(frame, CONF, 0.5)
                    saved_img = obj_model.draw(frame.copy(), objs)
                    if objs is not None and objs != [] and frame_counter % int(DURATION) == 0:
                        cv.imwrite(caught_pic_path, saved_img)
                else:
                    saved_img = frame

                flag, output = cv.imencode('.jpeg', saved_img)

                if frame_counter == int(cap.get(cv.CAP_PROP_FRAME_COUNT)):
                    frame_counter = 0
                    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                if flag:
                    yield b'--frame\r\n'
                    yield b'Content-Type: image/jpeg\r\n\r\n' + output.tobytes() + b'\r\n'


def send_warning_message():
    from twilio.rest import Client

    # 下面认证信息的值在你的 twilio 账户里可以找到
    account_sid = "AC8a544b650169b7a104a3053b99f8a073"
    auth_token = "dfa4b34db77d158cd6a2a8cad841845a"
    client = Client(account_sid, auth_token)

    message = client.messages.create(to="+8615221033591",  # 区号+你的手机号码
                                     from_="+18453828401",  # 你的 twilio 电话号码
                                     body="Warning!!! A person have fell down!!! Visit the Sit to Check. "
                                          "Send 1 to remove this warning. Send 0 to Call 120")
    print(message.sid)


def get_capture():
    global caught_pic_path, MESSAGE_SENT
    while True:
        if os.path.exists(caught_pic_path):
            if MESSAGE_SENT == 0:
                send_warning_message()
                MESSAGE_SENT = 1
            caught_pic = cv.imread(caught_pic_path)
            flag, output = cv.imencode('.jpeg', caught_pic)
            if flag:
                yield b'--frame\r\n'
                yield b'Content-Type: image/jpeg\r\n\r\n' + output.tobytes() + b'\r\n'
        else:
            error_img = cv.imread(f'{MEDIA_ROOT}/ErrorImage.jpg')
            flag, output = cv.imencode('.jpeg', error_img)
            if flag:
                yield b'--frame\r\n'
                yield b'Content-Type: image/jpeg\r\n\r\n' + output.tobytes() + b'\r\n'


@api_view(['GET'])
def get_caught_picture(request):
    if request.method == 'GET':
        return StreamingHttpResponse(get_capture(), content_type='multipart/x-mixed-replace; boundary=frame')


@api_view(['GET'])
def video_streamer(request):
    global CAM_ON
    if request.method == 'GET':
        cap = cv.VideoCapture(os.path.join(MEDIA_ROOT, 'my_test02.mp4'))

        # cap = cv.VideoCapture(0)
        if CAM_ON:
            return StreamingHttpResponse(get_video(cap), content_type='multipart/x-mixed-replace; boundary=frame')
    return Response(status=403)


@api_view(['POST'])
def set_detect_settings(request):
    global IS_DETECTED, CONF, CAM_ON
    data = request.data
    if data['isDetecting']:
        IS_DETECTED = True
    else:
        IS_DETECTED = False

    if data['isCamOn']:
        CAM_ON = True
    else:
        CAM_ON = False
    return Response(status=200)


@api_view(['GET'])
def recover_settings(request):
    return Response(data={'isDetecting': IS_DETECTED,
                          'isCamOn': CAM_ON,
                          'filter': CONF,
                          'duration': DURATION})


@api_view(['POST'])
def set_warning_settings(request):
    global CONF, DURATION
    data = request.data
    CONF = data['filter']
    DURATION = data['duration'],
    if isinstance(DURATION, tuple):
        DURATION = DURATION[0]
    return Response(status=200)


@api_view(['POST'])
def clear_cache(request):
    """
    TODO:清空缓存
    """
    global MESSAGE_SENT
    if os.path.exists(caught_pic_path):
        os.remove(caught_pic_path)
        MESSAGE_SENT = 0
        return Response(data={"message": "cached cleared"}, status=200)

    return Response(data={"message": "no cached to clear"})


@api_view(['POST'])
def cancel_alert(request):
    """
    TODO: 取消警报
    """
    pass
