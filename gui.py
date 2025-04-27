from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal
import threading
import sys
from screen_capture import capture_text_from_screenpipe, capture_text_once
from audio_capture import listen_and_transcribe
from summarizer import summarize_text
from utils import save_to_file

class AssistantGUI(QWidget):
    summary_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Meeting Summarizer")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.summary_box = QTextEdit(self)
        self.summary_box.setReadOnly(True)
        layout.addWidget(self.summary_box)

        self.start_btn = QPushButton("Start Summary", self)
        self.start_btn.clicked.connect(self.run_summary_thread)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

        self.summary_ready.connect(self.update_summary)

    def run_summary_thread(self):
        threading.Thread(target=self.summarize_live, daemon=True).start()

    def summarize_live(self):
        screen_text = capture_text_once()
        audio_text = listen_and_transcribe()
        full_text = screen_text + " " + audio_text

        print(f"DEBUG: full_text to summarize: {full_text}")
        summary = summarize_text(full_text)
        print(f"DEBUG: summary generated: {summary}")

        save_to_file(full_text, "output/transcript.txt")
        save_to_file(summary, "output/summary.txt")

        self.summary_ready.emit(summary)

    def update_summary(self, summary):
        self.summary_box.setPlainText(summary)

def run_gui():
    app = QApplication(sys.argv)
    gui = AssistantGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
