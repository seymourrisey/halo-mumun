from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '440')
Config.set('graphics', 'resizable', False)

import sys
import os
import json
import threading
import logging

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.text import LabelBase

import pystray
from PIL import Image as PILImage

import speech_recognition as sr
from core.config import save_api_key, load_api_key, is_valid_api_key
from core import mic






class InputAPIKeyScreen(Screen):
    def save_key(self):
        key = self.ids.api_input.text.strip()
        if key:
            save_api_key(key)
            self.manager.current = "main"


class SettingsScreen(Screen):
    def on_pre_enter(self):
        self.ids.status_label.text = ""
        current_key = load_api_key()
        if current_key:
            self.ids.api_input.text = current_key

    def save_key(self):
        new_key = self.ids.api_input.text.strip()
        if not new_key:
            self.ids.status_label.text = "API key tidak boleh kosong."
        elif not is_valid_api_key(new_key):
            self.ids.status_label.text = "Format API key tidak valid."
        else:
            save_api_key(new_key)
            self.ids.status_label.text = "API key disimpan!"
        Clock.schedule_once(self.clear_status_label, 2)

    def clear_status_label(self, dt):
        self.ids.status_label.text = ""


class MainScreen(Screen):
    is_listening = BooleanProperty(False)

    def animate_status_label(self, new_text):
        label = self.ids.status_label
        fade_out = Animation(opacity=0, duration=0.2)
        fade_in = Animation(opacity=1, duration=0.2)
        fade_out.bind(on_complete=lambda *x: setattr(label, 'text', new_text))
        fade_out.start(label)
        fade_out.bind(on_complete=lambda *x: fade_in.start(label))

    def set_mumun_thinking(self):
        Animation(opacity=0.3, duration=0.3).start(self.ids.mumun_image)

    def animate_mumun_speaking(self):
        self.ids.mumun_image.opacity = 0.2
        Animation(opacity=1, duration=0.4).start(self.ids.mumun_image)

    def mumun_idle(self):
        self.ids.mumun_image.opacity = 1

    def toggle_mic(self):
        if not self.is_listening:
            self.ids.mic_button.source = self.get_resource_path("ui/assets/icons/mic_pressed.png")
            self.animate_status_label("Mumun mulai mendengarkan...")
            self.is_listening = True
            mic.should_cancel = False
            threading.Thread(target=self.start_listening).start()
        else:
            mic.should_cancel = True
            self.ids.mic_button.source = self.get_resource_path("ui/assets/icons/mic.png")
            self.animate_status_label("Halo Mumun")
            self.is_listening = False

    def start_listening(self):
        user_text = mic.listen_once(timeout=5, phrase_time_limit=8)
        Clock.schedule_once(lambda dt: self.on_recognize_complete(user_text))

    def on_recognize_complete(self, user_text):
        self.ids.mic_button.source = self.get_resource_path("ui/assets/icons/mic.png")
        self.set_mumun_thinking()
        self.animate_status_label("Mumun sedang berpikir...")
        self.is_listening = False
        self.ids.mic_button.disabled = True
        self.ids.mic_button.opacity = 0.3
        logging.info(f"[USER SAID]: {user_text}")
        threading.Thread(target=self.process_ai_response, args=(user_text,)).start()

    def process_ai_response(self, user_text):
        from core.ai import get_gpt_response
        reply = get_gpt_response(user_text)
        Clock.schedule_once(lambda dt: self.mumun_reply(reply_text=reply))

    def mumun_reply(self, reply_text):
        self.animate_mumun_speaking()
        self.animate_status_label("Mumun berbicara...")
        print(f"[MUMUN]: {reply_text}")
        threading.Thread(target=self.run_tts, args=(reply_text,)).start()

    def run_tts(self, reply_text):
        from core.tts import speak
        import asyncio
        asyncio.run(speak(reply_text))
        Clock.schedule_once(self.reset_status_label, 1)
        self.ids.mic_button.disabled = True

    def reset_status_label(self, *args):
        self.animate_status_label("Halo  Mumun")
        self.ids.mic_button.disabled = False
        self.mumun_idle()
        self.ids.mic_button.opacity = 1

    def get_resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


class MumunApp(App):
    
    def get_resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def build(self):

        LabelBase.register(
            name="ModernDOS",
            fn_regular=self.get_resource_path("ui/assets/fonts/ModernDOS8x8.ttf")
        )

        Builder.load_file(self.get_resource_path("ui/style.kv"))
        
        sm = ScreenManager()
        sm.add_widget(InputAPIKeyScreen(name="input"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.current = "input" if not load_api_key() else "main"
        return sm

    def on_start(self):
        Window.bind(on_minimize=self.on_minimize)
        threading.Thread(target=self.run_tray_icon, daemon=True).start()

    def on_minimize(self, *args):
        Window.hide()
        return True

    def run_tray_icon(self):
        icon_path = self.get_resource_path("ui/assets/mumun.png")
        image = PILImage.open(icon_path)

        def on_quit(icon, item):
            icon.stop()
            App.get_running_app().stop()

        def show_window(icon, item):
            Clock.schedule_once(lambda dt: (Window.show(), Window.raise_window()))

        icon = pystray.Icon("Mumun", image, menu=pystray.Menu(
            pystray.MenuItem("Open Mumun", show_window),
            pystray.MenuItem("❌ Keluar", on_quit)
        ))
        icon.run()


if __name__ == "__main__":
    MumunApp().run()
