import shutil

from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
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


class HomeScreen(Screen):
    selection = ListProperty([])

    def load_txt(self):
        self.manager.ids.view_screen.ids.lb.text = self.ids.txt.text
        self.manager.current = 'view_screen'
        self.ids.txt.text = ''  # para limpar o input quando voltar pra essa tela

    def _set_image(self):
        splits = self.ids.image.source.split("\\")
        img_name = splits[len(splits) - 1]
        print(BASE_PATH + BASE_ANALYSIS_PATH + img_name)
        self.manager.ids.view_screen.ids.image2.source = BASE_PATH + BASE_ANALYSIS_PATH + img_name

    def submit_img(self):
        detect_thread = DetectThread(self.ids.image.source, self._set_image)
        detect_thread.daemon = True
        detect_thread.start()
        self.manager.current = 'view_screen'

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

    def close_application(self):
        App.get_running_app().stop()
        Window.close()


class ViewScreen(Screen):
    def change_screen(self):
        self.manager.current = 'home_screen'
        _clean_environment()


class FileChoose(Button):
    pass


class LabelDropDown(DropDown):
    pass


class Test(App):
    def build(self):
        return AppManager()


if __name__ == '__main__':
    try:
        _clean_environment()
    except:
        pass
    Test().run()
