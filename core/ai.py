import subprocess
import os
import sys

from core.config import load_api_key
import subprocess

TGPT_PATH = os.path.join("bin", "tgpt.exe")

DEFAULT_PREPROMPT = (
    "Nama kamu adalah 'Mumun'. Jawab dengan bahasa Indonesia. "
    "Gaya bicara santai, ngobrol, dan singkat. Sedikit judes tapi tetap ramah:"
)

STARTUPINFO = None
if sys.platform == "win32":
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def get_gpt_response(prompt: str) -> str:
    try:
        api_key = load_api_key()
        if not api_key:
            return "API key belum diatur. Silakan atur di menu Settings."

        command = [
            TGPT_PATH,
            "--provider", "groq",
            "--model", "meta-llama/llama-4-maverick-17b-128e-instruct",
            "--key", api_key,
            "--preprompt", DEFAULT_PREPROMPT,
            prompt
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            startupinfo=STARTUPINFO  # <- ini penting!
        )

        

        output = result.stdout.strip()
        lines = [line for line in output.splitlines() if len(line.strip()) > 20 and "Loading" not in line]
        reply = "\n".join(lines).strip()

        return reply or "Maaf, aku tidak bisa menjawab dengan benar."

    except Exception as e:
        print("[AI ERROR]", e)
        return "Maaf, terjadi kesalahan saat menghubungi AI."
