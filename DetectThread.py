import os
from threading import Thread

from Utils import BASE_PATH, BASE_ANALYSIS_PATH, LESIONED_ANALYSIS_PATH, NEGATIVE_ANALYSIS_PATH


class DetectThread(Thread):
    def __init__(self, img_source, callback):
        Thread.__init__(self)
        self.img_source = img_source
        self.callback = callback

    def run(self):
        os.system('python "' + BASE_PATH + 'detect.py" --weights "' + BASE_PATH + 'weights/best.pt" --name "' +
                  BASE_PATH + BASE_ANALYSIS_PATH + '" --img-size 1376 --source "' + self.img_source +
                  '" --augment --agnostic-nms --save-txt')
        os.system('python "' + BASE_PATH + 'detect.py" --weights "' + BASE_PATH + 'weights/best.pt" --name "' +
                  BASE_PATH + LESIONED_ANALYSIS_PATH + '" --img-size 1376 --source "' + self.img_source +
                  '" --augment --agnostic-nms --save-txt --classes 0')
        os.system('python "' + BASE_PATH + 'detect.py" --weights "' + BASE_PATH + 'weights/best.pt" --name "' +
                  BASE_PATH + NEGATIVE_ANALYSIS_PATH + '" --img-size 1376 --source "' + self.img_source +
                  '" --augment --agnostic-nms --save-txt --classes 1')
        self.callback()
