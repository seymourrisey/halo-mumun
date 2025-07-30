from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation


import speech_recognition as sr
import threading

from core.config import save_api_key, load_api_key, is_valid_api_key
from core import mic
from core.ai import get_gpt_response
from core.tts import speak

import logging

import os
import json


Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '440')
Config.set('graphics', 'resizable', False)

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

        def update_text(*args):
            label.text = new_text

        fade_out.bind(on_complete=update_text)
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
            #self.ids.mic_button.disabled = True
            self.ids.mic_button.source = "ui/assets/icons/mic_pressed.png"
            self.animate_status_label("Mumun mulai mendengarkan...")
            self.is_listening = True
            mic.should_cancel = False

            threading.Thread(target=self.start_listening).start()
        else:
            #self.ids.mic_button.disabled = True
            mic.should_cancel = True
            self.ids.mic_button.source = "ui/assets/icons/mic.png"
            self.animate_status_label("Halo Mumun")
            self.is_listening = False

    def start_listening(self):
        user_text = mic.listen_once(timeout=5, phrase_time_limit=8)
        Clock.schedule_once(lambda dt: self.on_recognize_complete(user_text))

    def on_recognize_complete(self, user_text):
        self.ids.mic_button.source = "ui/assets/icons/mic.png"
        self.set_mumun_thinking()
        self.animate_status_label("Mumun sedang berpikir...")
        self.is_listening = False
        self.ids.mic_button.disabled = True

        self.ids.mic_button.opacity = 0.3

        logging.basicConfig(level=logging.INFO)
        logging.info(f"[USER SAID]: {user_text}") 

        #Clock.schedule_once(lambda dt: self.mumun_reply(user_text=user_text), 2)
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

    # def mumun_reply(self, *args, user_text):
    #     self.animate_mumun_speaking()
    #     self.animate_status_label("Mumun berbicara...")
    #     if user_text.startswith("["):
    #         response = "Sepertinya ada gangguan saat mendengarkan kamu barusan."
    #     else:
    #         response = f"Kamu berkata: {user_text}"

    #     # Di sini kamu bisa jalankan edge-tts atau AI
    #     Clock.schedule_once(self.reset_status_label, 3)

    def reset_status_label(self, *args):
        self.animate_status_label("Halo  Mumun")
        self.ids.mic_button.disabled = False
        self.mumun_idle
        self.ids.mic_button.opacity = 1

                
class MumunApp(App):
    def build(self):
        Builder.load_file("ui/style.kv")
        sm = ScreenManager()

        sm.add_widget(InputAPIKeyScreen(name="input"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        
        if not load_api_key():
            sm.current = "input"
        else:
            sm.current = "main"

        return sm

if __name__ == "__main__":
    MumunApp().run()
