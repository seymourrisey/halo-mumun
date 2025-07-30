<p align="center">
  <img src="./mumun-tray.png" alt="MumunLogo" width="150"/>
</p>

#  Halo Mumun - GUI Edition

**Halo Mumun** adalah asisten AI ringan berbasis ChatGPT (via `tgpt`) dan Edge-TTS, kini hadir dalam antarmuka grafis (**GUI**) menggunakan **Kivy**. Dirancang sebagai aplikasi portable untuk Windows—langsung jalan, tanpa instalasi.

---

## ✨ Fitur

- ✅ Antarmuka GUI retro minimalis (font terminal)
- 🎤 Input suara via microphone (Speech Recognition)
- 🗣️ Balasan suara dengan Microsoft Edge TTS
- 🔑 Input dan simpan API Key langsung dari GUI
- 📌 Tray icon (minimize ke system tray)
- 📦 Portable – bisa dijalankan tanpa install

---

## 🚀 Cara Menjalankan (Versi Portable)

1. **Download file ZIP release**
2. **Ekstrak ke folder mana pun** (misalnya `C:\Mumun`)
3. Jalankan file:

```bash
MumunAI.exe
```

---
## 🔧 Build Sendiri (Opsional)

### 📦 Build EXE Portable
Jika kamu ingin build sendiri: 

1. Intall Dependency:
```bash
pip install -r requirement.txt
```
2. Build:
```bash
pyinstaller MumunAI.spec
```

---

## 🧠 Credits
- tgpt oleh [@aandrew-me](https://github.com/aandrew-me/tgpt)
- edge-tts oleh [@rany2](https://github.com/rany2/edge-tts)
- Microsoft TTS voices
- halo-mumun oleh [@seymourrisey](https://github.com/seymourrisey/halo-mumun)

---

## 📮 License

Proyek ini dirilis di bawah lisensi MIT.

Silakan digunakan, diubah, atau dikembangkan lebih lanjut sesuai kebutuhan—baik untuk pembelajaran, eksperimen, maupun integrasi ke dalam proyek Anda sendiri.