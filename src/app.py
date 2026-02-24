from kivy.uix.button import Button
from kivymd.app import MDApp


class App(MDApp):
    def build(self):
        return Button(text='Pickled Dictionary')