import os
from threading import Thread

from Utils import BASE_PATH_YOLO, BASE_ANALYSIS_PATH


class DetectThread(Thread):
    def __init__(self, img_source, callback):
        Thread.__init__(self)
        self.img_source = img_source
        self.callback = callback

    def run(self):
        os.system('python "' + BASE_PATH_YOLO + 'detect.py" --weights "' + BASE_PATH_YOLO + 'weights/best.pt" --name "' +
                  BASE_PATH_YOLO + BASE_ANALYSIS_PATH + '" --img-size 1376 --source "' + self.img_source +
                  '" --agnostic-nms --save-txt')
        self.callback()
