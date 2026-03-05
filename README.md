---
title: AI Meeting Assistant
emoji: 🎙️
colorFrom: indigo
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
---
# AI Meeting Assistant

Ses dosyalarından otomatik olarak Türkçe transkript, toplantı tutanağı ve görev listesi üreten çok ajanlı bir yapay zeka uygulaması. Google Gemini 1.5 Flash ve Gradio tabanlıdır.

---

## Docker ile Kurulum

### 1. Image'ı build edin

```bash
docker build -t ai-meeting-assistant .
```

### 2. Container'ı çalıştırın

```bash
docker run -p 7860:7860 --env-file .env ai-meeting-assistant
```

Uygulama `http://localhost:7860` adresinde açılır.

---

## Normal Kurulum

### 1. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 2. `.env` dosyası oluşturun

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Uygulamayı başlatın

```bash
python app.py
```
