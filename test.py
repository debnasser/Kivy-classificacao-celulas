import os
import shutil
from tkinter import *

import pandas as pd
from PIL import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from matplotlib import pyplot as plt, patches
from plyer import filechooser

from DetectThread import DetectThread
# noinspection PyUnresolvedReferences
from TooltipButton import TooltipButton
from Utils import BASE_PATH_YOLO, BASE_ANALYSIS_PATH, BASE_PATH

# Para gerar as imagens fora da thread principal
plt.switch_backend('agg')


def _clean_environment():
    shutil.rmtree(BASE_PATH_YOLO + BASE_ANALYSIS_PATH)
    os.remove(BASE_PATH + "images/all.png")
    os.remove(BASE_PATH + "images/lesioned.png")
    os.remove(BASE_PATH + "images/negative.png")
    os.remove(BASE_PATH + "images/original.png")


def _get_result(img_name, source):
    name = img_name[:-4]
    df = pd.read_csv(BASE_PATH_YOLO + BASE_ANALYSIS_PATH + "labels/" + name + ".txt", sep=" ",
                     names=["lesion", "x", "y", "width", "height"])
    df.sort_values(by=["lesion"], inplace=True)

    img = Image.open(source)
    img_width, img_height = img.size
    shapes_all = []
    shapes_lesion = []
    shapes_negative = []
    colors = [(1, 0, 0), (0, 0.298, 1)]
    for index, l in df.iterrows():
        color = colors[0] if l["lesion"] == 0 else colors[1]
        w = l["width"] * img_width
        h = l["height"] * img_height
        if l["lesion"] == 0:
            shapes_lesion.append(patches.Rectangle((l["x"] * img_width - (w / 2), l["y"] * img_height - (h / 2)), w, h,
                                                   edgecolor=color, facecolor='none', linewidth=2))
        else:
            shapes_negative.append(patches.Rectangle((l["x"] * img_width - (w / 2), l["y"] * img_height - (h / 2)), w,
                                                     h, edgecolor=color, facecolor='none', linewidth=2))
        shapes_all.append(patches.Rectangle((l["x"] * img_width - (w / 2), l["y"] * img_height - (h / 2)), w, h,
                                            edgecolor=color, facecolor='none', linewidth=2))
    names = ["original.png", "all.png", "lesioned.png", "negative.png"]

    for i in range(4):
        fig, ax = plt.subplots(figsize=(img_width / 100, img_height / 100))
        ax.imshow(img)

        if i == 0:
            shapes = []
        elif i == 1:
            shapes = shapes_all
        elif i == 2:
            shapes = shapes_lesion
        else:
            shapes = shapes_negative
        for s in shapes:
            ax.add_patch(s)

        plt.gca().set_axis_off()
        plt.margins(0, 0)
        plt.savefig(BASE_PATH + "images/" + names[i], bbox_inches='tight', pad_inches=0)
        plt.close()

    if df.iloc[0]["lesion"] == 0:
        return "Essa imagem foi classificada como: [color=ff0000]LESIONADA[/color]"
    else:
        return "Essa imagem foi classificada como: [color=004cff]NEGATIVA[/color]"


class AppManager(ScreenManager):
    pass


class HomeScreen(Screen):
    selection = ListProperty([])
    control = [False, False]

    def _set_image(self):
        splits = self.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.img_result_text.text = _get_result(img_name, self.ids.image.source)
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + "images/all.png"
        self.popup.dismiss()

    def submit_img(self):
        self.manager.current = 'view_screen'
        self.popup = WaitingPopUp()
        self.popup.open()
        detect_thread = DetectThread(self.ids.image.source, self._set_image)
        detect_thread.start()

    def choose(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        if self.selection == selection:
            self.on_selection()
        else:
            self.selection = selection

    def on_selection(self, *a, **k):
        try:
            self.ids.image.source = self.selection[0]
            self.ids.submit_button.disabled = False
            self.ids.file_choose.text = "Carregar outra imagem"
        except:
            pass

    def change_btn_status(self, pos, status):
        self.control[pos] = status
        result = False
        for c in self.control:
            result = result or c
        if result:
            Window.set_system_cursor("hand")
        else:
            Window.set_system_cursor("arrow")

    def close_application(self):
        App.get_running_app().stop()
        Window.close()


class ViewScreen(Screen):
    control = [False, False, False, False, False]

    def change_screen(self):
        self.manager.current = "home_screen"
        self.ids.image2.source = ""
        self.ids.img_result_text.text = ""
        _clean_environment()
        self.manager.ids.home_screen.ids.image.source = "images/fundo.png"
        self.manager.ids.home_screen.ids.file_choose.text = "Carregar uma imagem"
        self.manager.ids.home_screen.ids.submit_button.disabled = True

    def change_original(self):
        self.ids.image2.source = BASE_PATH + "images/original.png"

    def change_all(self):
        self.ids.image2.source = BASE_PATH + "images/all.png"

    def change_lesioned(self):
        self.ids.image2.source = BASE_PATH + "images/lesioned.png"

    def change_negative(self):
        self.ids.image2.source = BASE_PATH + "images/negative.png"

    def change_btn_status(self, pos, status):
        self.control[pos] = status
        result = False
        for c in self.control:
            result = result or c
        if result:
            Window.set_system_cursor("hand")
        else:
            Window.set_system_cursor("arrow")


class WaitingPopUp(Popup):
    pass


class Test(App):
    def build(self):
        self.title = "Citopathologist Eye Assistant"
        manager = AppManager()
        return manager


if __name__ == '__main__':
    try:
        _clean_environment()
    except:
        pass
    Test().run()
