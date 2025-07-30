import os
import time
import pygame
import asyncio
from edge_tts import Communicate

# Lokasi file audio TTS
TTS_DIR = os.path.join("data", "tts")
AUDIO_FILE = os.path.join(TTS_DIR, "audio.mp3")

# Pastikan folder tts tersedia
os.makedirs(TTS_DIR, exist_ok=True)

async def speak(text: str):
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    communicate = Communicate(text=text, voice="su-ID-TutiNeural")
    await communicate.save(AUDIO_FILE)

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()
