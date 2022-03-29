import numpy as np
from .utils.augmentations import letterbox
from .models.experimental import attempt_load
import cv2 as cv
from .utils.general import (check_img_size,
                           non_max_suppression, set_logging)
import argparse
import os
import sys
from pathlib import Path
import random

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class ObjDetection:
    def __init__(self, weights, imgsz=None) -> None:
        if imgsz is None:
            imgsz = [640, 640]
        set_logging()
        self.img_size = imgsz
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.half = self.device.type != 'cpu'
        model = attempt_load(weights, map_location=self.device)
        self.stride = max(int(model.stride.max()), 32)  # model stride
        self.names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        model.float()
        self.img_size = check_img_size(self.img_size, s=self.stride)
        self.model = model

    @property
    def class_labels(self) -> list:
        return self.names

    def __call__(self, *args, **kwds) -> list:
        return self.detect(*args, **kwds)

    @torch.no_grad()
    def detect(self, src, conf_thres=0.25, iou_thres=0.45, agnostic_nms=False, classes=None):
        img = letterbox(src, self.img_size, stride=self.stride, auto=True)[0]

        new_height, new_width = img.shape[:2]

        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        im = img.float()

        im /= 255
        if len(im.shape) == 3:
            im = im[None]

        pred = self.model(im, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms)
        items = []

        if pred[0] is not None and len(pred):
            for p in pred[0]:
                score = np.round(p[4].cpu().detach().numpy(), 2)
                label = self.names[int(p[5])]
                xmin = int(p[0] * src.shape[1] / self.img_size[0])
                ymin = int(p[1] * src.shape[0] / new_height)
                xmax = int(p[2] * src.shape[1] / self.img_size[0])
                ymax = int(p[3] * src.shape[0] / new_height)

                item = {'label': label,
                        'bbox': [(xmin, ymin), (xmax, ymax)],
                        'score': score
                        }

                items.append(item)

        return items

    def draw(self, src, objs):
        object_colors = [[0, 0, 255]]
        for obj in objs:
            # print(obj)
            label = obj['label']
            score = obj['score']
            [(xmin, ymin), (xmax, ymax)] = obj['bbox']
            color = object_colors[self.class_labels.index(label)]
            src = cv.rectangle(src, (xmin, ymin), (xmax, ymax), color, 2)
            src = cv.putText(src, f'{label} ({str(score)})', (xmin, ymin),
                             cv.FONT_HERSHEY_SIMPLEX, 0.75, color, 1, cv.LINE_AA)
        return src


if __name__ == "__main__":
    cap = cv.VideoCapture('test_video.avi')

    obj_model = ObjDetection("weights/best.pt", [480, 480])

    test_pic_dir = '/home/michael/dataset/test_fall_pic'

    count = 0
    for img_path in os.listdir(test_pic_dir):
        test_pic = os.path.join(test_pic_dir, img_path)
        image = cv.imread(test_pic)
        objs = obj_model(image, 0.70, 0.5)
        saved_img = obj_model.draw(image.copy(), objs)
        cv.imwrite(f'./runs/detect/exp5/frame{count}.png', saved_img)
        print(f'frame{count}.png saved')
        count += 1
