import os
import shutil

import pandas as pd
from PIL import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from matplotlib import pyplot as plt, patches
from plyer import filechooser

from DetectThread import DetectThread
from Utils import BASE_PATH_YOLO, BASE_ANALYSIS_PATH, BASE_PATH


def _clean_environment():
    shutil.rmtree(BASE_PATH_YOLO + BASE_ANALYSIS_PATH)
    os.remove(BASE_PATH + "images/all.png")
    os.remove(BASE_PATH + "images/lesioned.png")
    os.remove(BASE_PATH + "images/negative.png")
    os.remove(BASE_PATH + "images/original.png")


class AppManager(ScreenManager):
    pass


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
    colors = [(1, 0, 0), (0 / 255, 76 / 255, 1)]
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
        plt.savefig("D:/Projects/Kivy-classificacao-celulas/images/" + names[i], bbox_inches='tight', pad_inches=0)
        plt.close()

    if df.iloc[0]["lesion"] == 0:
        return "Essa imagem foi classificada como: LESIONADA"
    else:
        return "Essa imagem foi classificada como: NEGATIVA"


class HomeScreen(Screen):
    selection = ListProperty([])

    def _set_image(self):
        splits = self.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.img_result_text.text = _get_result(img_name, self.ids.image.source)
        self.manager.ids.view_screen.ids.image2.source = "D:/Projects/Kivy-classificacao-celulas/images/all.png"
        self.popup.dismiss()

    def submit_img(self):
        self.manager.current = 'view_screen'
        self.popup = WaitingPopUp()
        self.popup.open()
        detect_thread = DetectThread(self.ids.image.source, self._set_image)
        detect_thread.start()

    def selected(self, file):
        try:
            self.ids.image.source = file[0]
        except:
            pass

    def choose(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        self.selection = selection

    def on_selection(self, *a, **k):
        self.ids.image.source = self.selection[0]
        self.ids.submit_button.disabled = False

    def close_application(self):
        App.get_running_app().stop()
        Window.close()


class ViewScreen(Screen):
    def change_screen(self):
        self.manager.current = 'home_screen'
        _clean_environment()
        self.manager.ids.view_screen.ids.image2.source = ''
        self.manager.ids.view_screen.ids.img_result_text.text = ''

    def change_original(self):
        self.manager.ids.view_screen.ids.image2.source = "D:/Projects/Kivy-classificacao-celulas/images/original.png"

    def change_geral(self):
        self.manager.ids.view_screen.ids.image2.source = "D:/Projects/Kivy-classificacao-celulas/images/all.png"

    def change_lesioned(self):
        self.manager.ids.view_screen.ids.image2.source = "D:/Projects/Kivy-classificacao-celulas/images/lesioned.png"

    def change_negative(self):
        self.manager.ids.view_screen.ids.image2.source = "D:/Projects/Kivy-classificacao-celulas/images/negative.png"


class FileChoose(Button):
    pass


class LabelDropDown(DropDown):
    pass


class WaitingPopUp(Popup):
    pass


class Test(App):
    def build(self):
        self.title = "Citopathologist Eye Assistant"
        return AppManager()


if __name__ == '__main__':
    try:
        _clean_environment()
    except:
        pass
    Test().run()
