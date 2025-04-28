from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSignal
import threading
import sys
from screen_capture import capture_text_once
from audio_capture import listen_and_transcribe
from summarizer import summarize_text, answer_question
from utils import save_to_file

class AssistantGUI(QWidget):
    summary_ready = pyqtSignal(str)
    answer_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GlassEye Chatbot")
        self.setGeometry(200, 200, 600, 600)

        layout = QVBoxLayout()

        self.summary_box = QTextEdit(self)
        self.summary_box.setReadOnly(True)
        layout.addWidget(QLabel("Summary:"))
        layout.addWidget(self.summary_box)

        self.start_btn = QPushButton("Start Summary", self)
        self.start_btn.clicked.connect(self.run_summary_thread)
        layout.addWidget(self.start_btn)

        self.question_input = QLineEdit(self)
        self.question_input.setPlaceholderText("Enter your question here")
        layout.addWidget(QLabel("Ask a question:"))
        layout.addWidget(self.question_input)

        self.ask_btn = QPushButton("Get Answer", self)
        self.ask_btn.clicked.connect(self.run_qa_thread)
        layout.addWidget(self.ask_btn)

        self.answer_box = QTextEdit(self)
        self.answer_box.setReadOnly(True)
        layout.addWidget(QLabel("Answer:"))
        layout.addWidget(self.answer_box)

        self.setLayout(layout)

        self.summary_ready.connect(self.update_summary)
        self.answer_ready.connect(self.update_answer)

        self.captured_text = ""

    def run_summary_thread(self):
        threading.Thread(target=self.summarize_live, daemon=True).start()

    def summarize_live(self):
        screen_text = capture_text_once()
        audio_text = listen_and_transcribe()
        full_text = screen_text + " " + audio_text
        self.captured_text = full_text

        print(f"DEBUG: full_text to summarize: {full_text}")
        summary = summarize_text(full_text)
        print(f"DEBUG: summary generated: {summary}")

        save_to_file(full_text, "output/transcript.txt")
        save_to_file(summary, "output/summary.txt")

        self.summary_ready.emit(summary)

    def run_qa_thread(self):
        question = self.question_input.text().strip()
        if not question:
            self.answer_ready.emit("Please enter a question.")
            return
        threading.Thread(target=self.answer_question_thread, args=(question,), daemon=True).start()

    def answer_question_thread(self, question):
        if not self.captured_text:
            self.answer_ready.emit("No captured text available. Please start summary first.")
            return
        answer = answer_question(self.captured_text, question)
        self.answer_ready.emit(answer)

    def update_summary(self, summary):
        self.summary_box.setPlainText(summary)

    def update_answer(self, answer):
        self.answer_box.setPlainText(answer)

def run_gui():
    app = QApplication(sys.argv)
    gui = AssistantGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
