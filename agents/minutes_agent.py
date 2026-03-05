"""
Tutanak Ajanı
-------------
Toplantı transkriptinden resmi Türkçe toplantı tutanağı oluşturur.
Sadece google-genai SDK kullanır.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

MINUTES_PROMPT = """Aşağıdaki toplantı transkriptinden resmi bir Türkçe toplantı tutanağı oluştur.

Çıktı formatı (Markdown):
# Toplantı Tutanağı

## Toplantı Özeti
(2-3 cümle ile toplantının genel konusu ve amacı)

## Ana Gündem Maddeleri
(Konuşulan başlıca konuları maddeler halinde listele)

## Alınan Kararlar
(Toplantıda mutabık kalınan kararları listele. Karar alınmamışsa "Bu toplantıda resmi karar alınmamıştır." yaz.)

## Önemli Notlar
(Dikkat çekici bilgiler, uyarılar veya vurgulanan noktalar)

## Sonraki Adımlar
(Gelecekte yapılacaklar, planlanan toplantılar vb.)

---
Transkript:
{transcript}"""


def generate_minutes(transcript: str) -> str:
    """
    Transkriptten Türkçe toplantı tutanağı oluşturur.

    Args:
        transcript: Toplantı transkripti metni.

    Returns:
        Markdown formatında toplantı tutanağı.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını oluşturun."
        )

    if not transcript or not transcript.strip():
        raise ValueError("Transkript boş. Önce ses dosyasını işleyin.")

    client = genai.Client(api_key=api_key)
    prompt = MINUTES_PROMPT.format(transcript=transcript)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
