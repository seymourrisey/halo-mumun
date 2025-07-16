import os
from dotenv import load_dotenv
import asyncio
import threading
import time
import pygame
import speech_recognition as sr
import subprocess
from edge_tts import Communicate
import pystray
from PIL import Image

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def listen_and_transcribe():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    with sr.Microphone() as source:
        print("🎙️ Mumun sedang mendengarkan... Bicara sekarang.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="id-ID")
        print("📢 Kamu bilang:", text)
        return text
    except sr.UnknownValueError:
        print("😕 Mumun tidak mengerti.")
    except sr.RequestError as e:
        print(f"❌ Error pada Speech Recognition: {e}")
    return ""

def get_gpt_response(prompt):
    try:
        tgpt_path = "E:/Project/mumun/tgpt.exe"
        command = [
            tgpt_path,
            "--provider", "groq",
            "--model", "meta-llama/llama-4-maverick-17b-128e-instruct",
            "--key", GROQ_API_KEY,
            "--preprompt", "Nama kamu adalah 'Mumun'. Jawab dengan bahasa Indonesia. gaya berbicara santai, ngobrol, dan singkat. dan agak judes:",
            prompt
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        full_output = result.stdout.strip()
        lines = full_output.splitlines()
        clean_lines = [line for line in lines if len(line.strip()) > 20 and "Loading" not in line]
        reply = "\n".join(clean_lines).strip()
        return reply or "Maaf, aku tidak bisa menjawab dengan benar."
    except Exception as e:
        print("❌ Gagal mendapatkan respon dari GPT:", e)
        return "Maaf, aku tidak bisa menjawab sekarang."

async def speak(text):
    mp3_file = "output.mp3"
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    communicate = Communicate(text=text, voice="su-ID-TutiNeural")
    await communicate.save(mp3_file)
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()

def play_cue_sound():
    cue_file = "blip.wav"
    if pygame.mixer.get_init():
        pygame.mixer.quit()
    pygame.mixer.init()
    pygame.mixer.music.load(cue_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()

def run_listen():
    text = listen_and_transcribe()
    if text:
        user_input = text
        print("⌛ Mumun sedang mikir...")
        reply = get_gpt_response(user_input)
        print("🤖 Mumun menjawab:", reply)
        asyncio.run(speak(reply))

def run_with_cue():
    play_cue_sound()
    run_listen()

def on_exit(icon, item):
    icon.stop()

def create_image():
    return Image.open("mumun-tray.png")

menu = pystray.Menu(
    pystray.MenuItem("🎤 Mulai Dengarkan", lambda icon, item: threading.Thread(target=run_with_cue).start()),
    pystray.MenuItem("❌ Keluar", on_exit)
)

icon = pystray.Icon("Mumun", icon=create_image(), title="Mumun AI Assistant", menu=menu)
icon.run()
