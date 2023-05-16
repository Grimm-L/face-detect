from django.http import HttpResponse
from django.shortcuts import render
import json

try:
    from detect.ai.db import parse_menu_info_from_redis
    from detect.ai.front import Front
    import redis

    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set("has_detect", "0")
    r.set("has_override", "0")
    r.set("has_modify", "0")
    detector = Front()
    last_menu_fingerprint = "placeholder"
except ImportError:
    print("Import Error, Web Development Mode")


def detect(request):
    global last_menu_fingerprint

    if request.method != 'POST':
        return HttpResponse("<h1>Please POST!</h1>")

    if int(r.get("has_detect")) == 0:
        print("detecting...")
        image = request.FILES.get('file').read()
        menu = detector.get_face_menu(image, face_thre=1.0, fix_bbox_thre=200, fix_frame_thre=2)
        print("Current Menu:", menu)
        print("Receive Image Size:", request.FILES.get('file').size)
        if menu is not None:
            r.set("has_detect", "1")
            r.set("has_override", "0")
            r.set("has_modify", "0")
            last_menu_fingerprint = menu[1]
            return render(request, 'faceui/index_override.html', menu[0])
        else:
            return HttpResponse("empty")
    elif int(r.get("has_override")) == 1 or int(r.get("has_modify")) == 1:
        print("manual modify the menu... override")
        menu, menu_fingerprint = parse_menu_info_from_redis()
        if menu_fingerprint != last_menu_fingerprint:
            last_menu_fingerprint = menu_fingerprint
            return render(request, 'faceui/index_override.html', menu)
        else:
            return HttpResponse("no change")
    else:
        return HttpResponse("no change")


def detect_dev_api(request):
    if request.method != 'POST':
        return HttpResponse("<h1>Please POST!</h1>")

    # 路径需要改成接口返回数据的路径
    with open("C:/Users/56469/Code/Face/test.json", "r") as f:
        menu_content = json.loads(f.read())

    # 该接口有三种返回情况，调试时通过注释掉不同的情况来测试
    # 1. 本次识别成功，返回使用当前 menu 渲染的整个页面，进入页面锁定状态（不再继续识别）
    return render(request, 'faceui/index_override.html', menu_content)

    # 2. 已经识别成功并且锁定状态未解除，返回 no change 让页面不要做任何更改
    # return HttpResponse("no change")

    # 3. 本次识别失败，返回 empty，同样页面不做任何更改
    # return HttpResponse("empty")

def menu_api_demo(request):
    with open("C:/Users/56469/Code/Face/test.json", "r") as f:
        menu = f.read()
    return HttpResponse(menu)
