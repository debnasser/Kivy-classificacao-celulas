import shutil

import pandas as pd
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from plyer import filechooser

from DetectThread import DetectThread
from Utils import BASE_PATH, BASE_ANALYSIS_PATH, NEGATIVE_ANALYSIS_PATH, LESIONED_ANALYSIS_PATH


def _clean_environment():
    shutil.rmtree(BASE_PATH + BASE_ANALYSIS_PATH)
    shutil.rmtree(BASE_PATH + NEGATIVE_ANALYSIS_PATH)
    shutil.rmtree(BASE_PATH + LESIONED_ANALYSIS_PATH)


class AppManager(ScreenManager):
    pass


def _get_result(img_name):
    name = img_name[:-4]
    df = pd.read_csv(BASE_PATH + BASE_ANALYSIS_PATH + "labels/" + name + ".txt", sep=" ",
                     names=["lesion", "x", "y", "width", "heigth"])
    df.sort_values(by=["lesion"], inplace=True)
    if df.iloc[0]["lesion"] == 0:
        return "Essa imagem foi classificada como: LESIONADA"
    else:
        return "Essa imagem foi classificada como: NEGATIVA"


class HomeScreen(Screen):
    selection = ListProperty([])

    def _set_image(self):
        splits = self.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + BASE_ANALYSIS_PATH + img_name
        self.manager.ids.view_screen.ids.img_result_text.text = _get_result(img_name)
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
        self.manager.ids.view_screen.ids.image2.source = self.manager.ids.home_screen.ids.image.source

    def change_geral(self):
        splits = self.manager.ids.home_screen.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + BASE_ANALYSIS_PATH + img_name

    def change_lesioned(self):
        splits = self.manager.ids.home_screen.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + LESIONED_ANALYSIS_PATH + img_name

    def change_negative(self):
        splits = self.manager.ids.home_screen.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + NEGATIVE_ANALYSIS_PATH + img_name


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