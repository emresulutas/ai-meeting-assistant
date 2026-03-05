"""
Transkript Ajanı
----------------
Ses dosyasını Gemini Files API'ye yükler ve Türkçe metne dönüştürür.
Yerel model (Whisper vb.) KULLANILMAZ — sadece google-genai SDK.
"""

import os
import time
import mimetypes
from google import genai
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_AUDIO_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mp3",
    ".aiff": "audio/aiff",
    ".aac": "audio/aac",
    ".ogg": "audio/ogg",
    ".flac": "audio/flac",
    ".m4a": "audio/mp4",
}

TRANSCRIPT_PROMPT = """Bu ses kaydını tam ve eksiksiz olarak Türkçe metne dök.
Kurallar:
- Ses kaydındaki her şeyi yaz, hiçbir şeyi atlama.
- Konuşmacıları ayırt edebiliyorsan [Konuşmacı 1]:, [Konuşmacı 2]: formatında belirt.
- Türkçe olmayan ifadeler varsa olduğu gibi yaz, çevirme.
- Anlaşılmayan kısımları [anlaşılmıyor] olarak işaretle.
Sadece transkripti yaz, başka açıklama ekleme."""


def _get_mime_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext in SUPPORTED_AUDIO_TYPES:
        return SUPPORTED_AUDIO_TYPES[ext]
    guessed, _ = mimetypes.guess_type(file_path)
    if guessed and guessed.startswith("audio/"):
        return guessed
    raise ValueError(
        f"Desteklenmeyen dosya formatı: {ext}. "
        f"Desteklenen formatlar: {', '.join(SUPPORTED_AUDIO_TYPES.keys())}"
    )


def transcribe_audio(audio_path: str, progress_callback=None) -> str:
    """
    Ses dosyasını Gemini API ile Türkçe metne dönüştürür.

    Args:
        audio_path: Ses dosyasının tam yolu.
        progress_callback: İsteğe bağlı ilerleme bildirimi fonksiyonu.

    Returns:
        Türkçe transkript metni.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını oluşturun."
        )

    mime_type = _get_mime_type(audio_path)
    client = genai.Client(api_key=api_key)

    if progress_callback:
        progress_callback("Ses dosyası Gemini'ye yükleniyor...")

    uploaded_file = client.files.upload(
        file=audio_path,
        config={"mime_type": mime_type},
    )

    # Dosyanın işlenmesini bekle
    wait_seconds = 0
    while uploaded_file.state.name == "PROCESSING":
        if wait_seconds > 300:
            raise TimeoutError("Dosya işleme 5 dakikayı aştı.")
        time.sleep(5)
        wait_seconds += 5
        uploaded_file = client.files.get(name=uploaded_file.name)
        if progress_callback:
            progress_callback(f"Dosya işleniyor... ({wait_seconds}s)")

    if uploaded_file.state.name == "FAILED":
        raise RuntimeError("Dosya Gemini tarafından işlenemedi.")

    if progress_callback:
        progress_callback("Transkript oluşturuluyor...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[uploaded_file, TRANSCRIPT_PROMPT],
    )

    # Temizlik: yüklenen dosyayı sil
    try:
        client.files.delete(name=uploaded_file.name)
    except Exception:
        pass  # Temizlik hatası kritik değil

    return response.text
