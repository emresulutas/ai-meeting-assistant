---
title: AI Meeting Assistant
emoji: 🎙️
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
# AI Meeting Assistant

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/emresulutas/ai-meeting-assistant)

A multi-agent AI application that automatically generates Turkish transcripts, meeting minutes, and task lists from audio files. Built with Google Gemini 2.5 Flash and Gradio.

---

## Setup with Docker

### 1. Build the image

```bash
docker build -t ai-meeting-assistant .
```

### 2. Run the container

```bash
docker run -p 7860:7860 --env-file .env ai-meeting-assistant
```

The application will be available at `http://localhost:7860`.

---

## Standard Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Start the application

```bash
python app.py
```

# AI Meeting Assistant

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/emresulutas/ai-meeting-assistant)

Ses dosyalarından otomatik olarak Türkçe transkript, toplantı tutanağı ve görev listesi üreten çok ajanlı bir yapay zeka uygulaması. Google Gemini 2.5 Flash ve Gradio tabanlıdır.

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
