from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
import threading
import sys
from screen_capture import capture_text_from_screenpipe
from audio_transcribe import listen_and_transcribe
from summarizer import generate_summary
from utils import save_to_file

class AssistantGUI(QWidget):
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

    def run_summary_thread(self):
        threading.Thread(target=self.summarize_live, daemon=True).start()

    def summarize_live(self):
        screen_text = capture_text_from_screenpipe()
        audio_text = listen_and_transcribe()
        full_text = screen_text + " " + audio_text

        summary = generate_summary(full_text)

        save_to_file(full_text, "output/transcript.txt")
        save_to_file(summary, "output/summary.txt")

        self.summary_box.setPlainText(summary)

def run_gui():
    app = QApplication(sys.argv)
    gui = AssistantGUI()
    gui.show()
    sys.exit(app.exec_())
