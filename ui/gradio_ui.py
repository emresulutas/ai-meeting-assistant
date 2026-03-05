"""
Gradio UI — Orkestratör
-----------------------
Kullanıcıdan ses alır, sırasıyla Transkript → Tutanak → Görev akışını
işletir, sonuçları ekranda gösterir ve Markdown dosyası olarak dışa aktarır.
"""

import os
import tempfile
from datetime import datetime

import gradio as gr
from agents import transcribe_audio, generate_minutes, generate_tasks


def process_meeting(audio_path: str, progress=gr.Progress()):
    """
    Ana orkestrasyon fonksiyonu.
    Gradio'dan ses dosyasının geçici yolunu alır, ajanları sırayla çağırır.
    """
    if audio_path is None:
        raise gr.Error("Lütfen bir ses dosyası yükleyin.")

    # --- Aşama 1: Transkript ---
    progress(0.1, desc="Ses dosyası yükleniyor...")

    def transcript_progress(msg: str):
        progress(0.2, desc=msg)

    try:
        transcript = transcribe_audio(audio_path, progress_callback=transcript_progress)
    except EnvironmentError as e:
        raise gr.Error(str(e))
    except ValueError as e:
        raise gr.Error(f"Dosya formatı hatası: {e}")
    except Exception as e:
        raise gr.Error(f"Transkript oluşturulurken hata: {e}")

    progress(0.45, desc="Transkript hazır. Tutanak oluşturuluyor...")

    # --- Aşama 2: Tutanak ---
    try:
        minutes = generate_minutes(transcript)
    except Exception as e:
        raise gr.Error(f"Tutanak oluşturulurken hata: {e}")

    progress(0.70, desc="Tutanak hazır. Görev listesi oluşturuluyor...")

    # --- Aşama 3: Görev Listesi ---
    try:
        tasks = generate_tasks(transcript)
    except Exception as e:
        raise gr.Error(f"Görev listesi oluşturulurken hata: {e}")

    progress(0.90, desc="Markdown dosyası hazırlanıyor...")

    # --- Aşama 4: Markdown Export ---
    md_path = _export_markdown(transcript, minutes, tasks)

    progress(1.0, desc="Tamamlandı!")

    return transcript, minutes, tasks, md_path


def _export_markdown(transcript: str, minutes: str, tasks: str) -> str:
    """Üç çıktıyı tek bir Markdown dosyasına birleştirir."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"toplanti_tutanagi_{timestamp}.md"

    content = f"""# AI Toplantı Asistanı Raporu
*Oluşturulma: {datetime.now().strftime("%d.%m.%Y %H:%M")}*

---

# Transkript

{transcript}

---

{minutes}

---

{tasks}
"""

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


def create_ui() -> gr.Blocks:
    """Gradio Blocks arayüzünü oluşturur ve döner."""

    with gr.Blocks(title="AI Toplantı Asistanı") as app:

        gr.Markdown(
            """
# AI Toplantı Asistanı
**Powered by Gemini 2.5 Flash** | Ses kaydınızı yükleyin, gerisini halledelim.
"""
        )

        with gr.Row():
            # Sol sütun: yükleme
            with gr.Column(scale=1):
                gr.Markdown("### Ses Dosyası")
                audio_input = gr.Audio(
                    label="Toplantı Kaydı",
                    type="filepath",
                    sources=["upload"],
                )
                gr.Markdown(
                    "_Desteklenen formatlar: wav, mp3, ogg, flac, aac, m4a, aiff_",
                    elem_classes="small-text",
                )
                process_btn = gr.Button(
                    "Toplantıyı İşle",
                    variant="primary",
                    size="lg",
                )
                status_box = gr.Textbox(
                    label="Durum",
                    interactive=False,
                    value="Ses dosyası bekleniyor...",
                    lines=2,
                )

            # Sağ sütun: çıktılar
            with gr.Column(scale=2):
                gr.Markdown("### Sonuçlar")
                with gr.Tabs():
                    with gr.TabItem("Transkript"):
                        transcript_out = gr.Markdown(
                            value="_Henüz işlem yapılmadı._",
                            elem_classes="output-tab",
                        )
                    with gr.TabItem("Toplantı Tutanağı"):
                        minutes_out = gr.Markdown(
                            value="_Henüz işlem yapılmadı._",
                            elem_classes="output-tab",
                        )
                    with gr.TabItem("Görev Listesi"):
                        tasks_out = gr.Markdown(
                            value="_Henüz işlem yapılmadı._",
                            elem_classes="output-tab",
                        )

        with gr.Row():
            download_btn = gr.DownloadButton(
                label="Markdown Olarak İndir (.md)",
                variant="secondary",
                visible=False,
            )

        # Gizli state: dosya yolu
        md_file_state = gr.State(value=None)

        def on_process(audio_path, progress=gr.Progress()):
            transcript, minutes, tasks, md_path = process_meeting(audio_path, progress)
            return (
                transcript,
                minutes,
                tasks,
                "Tüm aşamalar tamamlandı. Dosyayı indirebilirsiniz.",
                gr.update(visible=True, value=md_path),
            )

        process_btn.click(
            fn=on_process,
            inputs=[audio_input],
            outputs=[transcript_out, minutes_out, tasks_out, status_box, download_btn],
            show_progress=True,
        )

    return app
