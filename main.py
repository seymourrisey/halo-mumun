from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.lang import Builder
Builder.load_file("ui/style.kv")

from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock


import os
import json

# Atur ukuran window
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '440')
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
    is_listening = BooleanProperty(False)

    def toggle_mic(self):
        if not self.is_listening:
            # START listening
            self.ids.mic_button.source = "ui/assets/icons/mic_pressed.png"
            self.ids.status_label.text = "Mumun mulai mendengarkan..."
            self.is_listening = True

            # Simulasi: delay lalu ke thinking
            Clock.schedule_once(self.on_listen_complete, 3)  # 3 detik simulasi rekam suara
        else:
            # STOP listening (kalau dipencet lagi)
            self.on_listen_complete()

    def on_listen_complete(self, *args):
        self.ids.mic_button.source = "ui/assets/icons/mic.png"
        self.ids.status_label.text = "Mumun sedang berpikir..."
        self.is_listening = False

        # Simulasi AI processing → lalu jawab
        Clock.schedule_once(self.mumun_reply, 2)

    def mumun_reply(self, *args):
        self.ids.status_label.text = "Mumun berbicara..."
        # Di sini kamu bisa jalankan edge-tts atau apapun

    

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
