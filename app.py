"""
AI Toplantı Asistanı — Giriş Noktası
"""

import gradio as gr
from ui.gradio_ui import create_ui

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0", # Docker için şart
        server_port=7860,      # Docker varsayılan portu
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
    )