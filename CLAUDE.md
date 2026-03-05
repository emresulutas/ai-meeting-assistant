# Proje Kuralları (Boris Kuralları)

## Temel Kural
Sistemde ses işleme ve metin işleme dahil **HER ŞEY** için sadece **Gemini API**
(`google-generativeai`) kullanılacaktır.

## Kesinlikle Yasak Bağımlılıklar
- HuggingFace (`transformers`, `diffusers`, vb.)
- OpenAI Whisper veya başka yerel ses modelleri
- PyTorch (`torch`, `torchaudio`)
- TensorFlow / Keras (yerel model için)
- `langchain` (bu projede gereksiz katman)

## İzin Verilen Bağımlılıklar
- `google-generativeai` — tüm AI işlemleri
- `gradio` — kullanıcı arayüzü
- `python-dotenv` — ortam değişkenleri

## Dil Kuralı
Tüm çıktılar (transkript, tutanak, görev listesi) daima **Türkçe** olacaktır.

## Mimari
- **Transkript Ajanı**: Ses → Gemini Files API → Türkçe metin
- **Tutanak Ajanı**: Metin → Gemini → Türkçe toplantı tutanağı
- **Görev Ajanı**: Metin → Gemini → Türkçe görev listesi
- **Orkestratör**: Gradio UI, akışı yönetir, Markdown export sağlar
