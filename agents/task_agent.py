"""
Görev Ajanı
-----------
Toplantı transkriptinden Türkçe görev listesi çıkarır.
Sadece google-genai SDK kullanır.
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

TASK_PROMPT = """Aşağıdaki toplantı transkriptinden tüm görevleri, sorumluları ve tarihleri çıkar.

Çıktı formatı (Markdown):
# Görev Listesi

## Atanan Görevler
(Her görev için aşağıdaki formatı kullan. Tarih belirtilmemişse "Tarih belirtilmemiş" yaz.)

- [ ] **[Görevin kısa adı]**
  - Açıklama: [Görevin detayı]
  - Sorumlu: [Kişi adı veya "Belirtilmemiş"]
  - Son Tarih: [Tarih veya "Belirtilmemiş"]

## Takip Edilecek Konular
(Görev olmayan ama takip gerektiren konular)

## Toplantı Bilgileri
- Toplam görev sayısı: [N]
- Sorumlu atanmış görevler: [N]
- Tarihi belirlenmiş görevler: [N]

---
Eğer transkriptte hiç görev veya aksiyon maddesi yoksa bunu açıkça belirt.

Transkript:
{transcript}"""


def generate_tasks(transcript: str) -> str:
    """
    Transkriptten Türkçe görev listesi oluşturur.

    Args:
        transcript: Toplantı transkripti metni.

    Returns:
        Markdown formatında görev listesi.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY bulunamadı. Lütfen .env dosyasını oluşturun."
        )

    if not transcript or not transcript.strip():
        raise ValueError("Transkript boş. Önce ses dosyasını işleyin.")

    client = genai.Client(api_key=api_key)
    prompt = TASK_PROMPT.format(transcript=transcript)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
