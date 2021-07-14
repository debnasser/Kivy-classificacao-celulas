import os
import kivy 
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import ListProperty
from plyer import filechooser
import shutil

class TelaManager(ScreenManager):
    pass

class Screen1(Screen):
    def load_txt(self):        
        self.manager.ids.screen2.ids.lb.text = self.ids.txt.text
        self.manager.current = 'screen2'
        self.ids.txt.text = ''      # para limpar o input quando voltar pra essa tela

    def classificar_img(self):
        print("cliquei")
        os.system('python "C:/Users/xr4good/Desktop/Kivy-classificacao-celulas/yolov5/detect.py" --weights "C:/Users/xr4good/Desktop/Kivy-classificacao-celulas/yolov5/weights/best.pt" --name "C:/Users/xr4good/Desktop/Kivy-classificacao-celulas/yolov5/runs/detect/exp/" --img-size 1376 --source "'+self.ids.image.source+'" --augment --agnostic-nms --save-txt')
        self.manager.current = 'screen2'
        self.manager.ids.screen2.ids.image2.source = "C:\\Users\\xr4good\\Desktop\\Kivy-classificacao-celulas\\yolov5\\runs\\detect\\exp\\"+self.ids.image.source.split("\\")[len(self.ids.image.source.split("\\"))-1:][0]
        
    def selected(self, file):
        try:
            self.ids.image.source = file[0]
            print(file[0])
        except:
            pass
        
    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection
        print(selection)

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        print("selection")
        print(self.selection[0])
        self.ids.image.source = self.selection[0]
        #App.get_running_app().root.ids.result.text = str(self.selection)

    def close_application(self):
        # closing application
        App.get_running_app().stop()
        #os.remove('C:\\Users\\xr4good\\Desktop\\Kivy-classificacao-celulas\\yolov5\\runs\\detect\\exp\\')
        # removing window
        Window.close()

class Screen2(Screen):
    def voltar_tela(self):
        self.manager.current = 'screen1'
        shutil.rmtree('C:\\Users\\xr4good\\Desktop\\Kivy-classificacao-celulas\\yolov5\\runs\\detect\\exp\\')
        

class FileChoose(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''
    pass 
    


#class FirstLayout(BoxLayout):
	
#    def load_text(self):
#        self.ids.label1.text='FUNCIONOU'
    
#    def clear(self):
#        self.remove_widget()
	
class Test(App):
    def build(self):          
        return TelaManager()
        #return FirstLayout()

try:
    shutil.rmtree('C:\\Users\\xr4good\\Desktop\\Kivy-classificacao-celulas\\yolov5\\runs\\detect\\exp\\')
except:
    pass
Test().run()
