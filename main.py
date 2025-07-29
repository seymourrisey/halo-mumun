from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.lang import Builder

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
    _listen_event = None

    def toggle_mic(self):
        if not self.is_listening:
            # START listening
            self.ids.mic_button.source = "ui/assets/icons/mic_pressed.png"
            self.ids.status_label.text = "Mumun mulai mendengarkan..."
            self.is_listening = True

            self._listen_event = Clock.schedule_once(self.on_listen_complete, 3)
        else:
            # STOP (cancel listening)
            if self._listen_event:
                self._listen_event.cancel()
                self._listen_event = None

            self.ids.mic_button.source = "ui/assets/icons/mic.png"
            self.ids.status_label.text = "Halo Mumun"
            self.is_listening = False


    def on_listen_complete(self, *args):
        self.ids.mic_button.source = "ui/assets/icons/mic.png"
        self.ids.status_label.text = "Mumun sedang berpikir..."
        self.is_listening = False
        self.ids.mic_button.disabled = True

        # Simulasi AI processing → lalu jawab
        Clock.schedule_once(self.mumun_reply, 2)

    def mumun_reply(self, *args):
        self.ids.status_label.text = "Mumun berbicara..."
        # Di sini kamu bisa jalankan edge-tts atau apapun
        Clock.schedule_once(self.reset_status_label, 3)

    def reset_status_label(self, *args):
        self.ids.status_label.text = "Halo  Mumun"
        self.ids.mic_button.disabled = False
    
class SettingsScreen(Screen):
    def on_pre_enter(self):
        self.ids.status_label.text = ""
        # Tampilkan API key saat ini (jika ada)
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                data = json.load(f)
                self.ids.api_input.text = data.get("groq_api_key", "")

    def save_key(self):
        new_key = self.ids.api_input.text.strip()
        if new_key:
            with open(CONFIG_PATH, "w") as f:
                json.dump({"groq_api_key": new_key}, f)
            self.ids.status_label.text = "API key disimpan!"
        else:
            self.ids.status_label.text = "API key tidak boleh kosong."

        Clock.schedule_once(self.clear_status_label, 2)

    def clear_status_label(self, dt):
        self.ids.status_label.text = ""

                
class MumunApp(App):
    def build(self):
        Builder.load_file("ui/style.kv")
        sm = ScreenManager()

        sm.add_widget(InputAPIKeyScreen(name="input"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))

        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    data = json.load(f)
                    if data.get("groq_api_key"):
                        sm.current = "main"
                    else:
                        sm.current = "input"
            except:
                sm.current = "input"
        else:
            sm.current = "input"

        return sm

if __name__ == "__main__":
    MumunApp().run()
