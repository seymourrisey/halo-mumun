from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.lang import Builder
Builder.load_file("ui/style.kv")

import os
import json

# Atur ukuran window
Config.set('graphics', 'width', '460')
Config.set('graphics', 'height', '540')
Config.set('graphics', 'resizable', False)

CONFIG_PATH = "data/mumun_config.json"

class InputAPIKeyScreen(Screen):
    def save_key(self):
        key = self.ids.api_input.text.strip()
        if key:
            os.makedirs("data", exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                json.dump({"groq_api_key": key}, f)
            self.manager.current = "main"

class MainScreen(Screen):
    def on_enter(self):
        self.ids.status_label.text = "Mumun siap mendengarkan..."

class MumunApp(App):
    def build(self):
        Builder.load_file("ui/style.kv")
        sm = ScreenManager()

        sm.add_widget(InputAPIKeyScreen(name="input"))
        sm.add_widget(MainScreen(name="main"))

        if not os.path.exists(CONFIG_PATH):
            sm.current = "input"
        else:
            sm.current = "main"

        return sm

if __name__ == "__main__":
    MumunApp().run()
