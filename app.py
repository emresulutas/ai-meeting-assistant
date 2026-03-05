"""
AI Toplantı Asistanı — Giriş Noktası
"""

import gradio as gr
from ui.gradio_ui import create_ui

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="127.0.0.1",  
        server_port=8080,         
        share=False,
        show_error=True,
        theme=gr.themes.Soft(),
    )