import speech_recognition as sr
import time

should_cancel = False

def listen_once(timeout=5, phrase_time_limit=10) -> str:
    global should_cancel
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Mumun mendengarkan...")
        recognizer.adjust_for_ambient_noise(source)

        end_time = time.time() + timeout
        while time.time() < end_time:
            if should_cancel:
                return "[Dibatalkan oleh pengguna]"

            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=phrase_time_limit)
                print("🧠 Mumun sedang mengenali suara...")
                if should_cancel:
                    return "[Dibatalkan oleh pengguna]"
                return recognizer.recognize_google(audio, language="id-ID")
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                return "Maaf, Mumun tidak bisa memahami suara kamu."
            except sr.RequestError as e:
                return f"Terjadi kesalahan saat meminta hasil pengenalan suara: {e}"

        return "Maaf, tidak ada suara terdeteksi."
    