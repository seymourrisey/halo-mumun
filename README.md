<p align="center">
  <img src="./mumun-tray.png" alt="MumunLogo" width="150"/>
</p>

#  Halo Mumun - AI Asisten Ngobrol Santai di System Tray

Proyek Python ringan untuk bikin AI asisten suara yang bisa diajak ngobrol pakai gaya santai. Mumun nongkrong di tray bar, siap dengerin dan ngerespon kamu kayak temen ngobrol.

---

## ✨ Fitur Utama

- 🎧 **Dengar suara kamu** via microphone (speech recognition)
- 🧠 **Jawab pertanyaan** pakai AI via tgpt + Groq API (model Meta Llama 4)
- 🔊 **Ngomong balik** pakai suara TTS Indonesia dari Edge TTS
- 📌 **Nongkrong di system tray** kayak asisten pribadi 
- 🎵 **Suara cue blip** saat mulai rekaman biar keren

---

## ⚙️ Cara Install dan Jalankan

> 💡 **Diperlukan Python versi 3.11** atau lebih baru agar kompatibel dengan semua dependensi.

### 🧾 1. Clone Reponya

```bash
git clone https://github.com/username/halo-mumun.git
cd halo-mumun
```
### 🧪 2. (Opsional) Buat Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  
```

### 📦 3. Install Semua Dependency

```bash
pip install -r requirements.txt
```

### 🔑 4. Dapatkan API Key dari Groq

 - Buka: https://console.groq.com
 - Daftar / login
 - Salin API Key kamu

### 📝 5. Isi File .env

Buat file .env (jika belum ada), lalu isi:
```bash
GROQ_API_KEY=gsk_KEY_ANDA
# Masukkan API key dari Groq di atas
```
---

## ▶️ Cara Menjalankan Mumun

Lewat python script 
```bash
python mumun.py
```
atau 

Jalankan file 
```bash
MumunAI.exe
```

---

## 🧠 Credits
- tgpt oleh [@aandrew-me](https://github.com/aandrew-me/tgpt)
- edge-tts oleh [@rany2](https://github.com/rany2/edge-tts)
- Microsoft TTS voices

## 📮 License

Proyek ini dirilis di bawah lisensi MIT.

Silakan digunakan, diubah, atau dikembangkan lebih lanjut sesuai kebutuhan—baik untuk pembelajaran, eksperimen, maupun integrasi ke dalam proyek Anda sendiri.
