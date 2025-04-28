from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QGroupBox, QSizePolicy, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt
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
        self.setGeometry(200, 200, 700, 700)

        self.captured_text = ""

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Stacked widget to switch between choice, summary, and QA views
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Choice widget
        choice_widget = QWidget()
        choice_layout = QVBoxLayout()
        choice_widget.setLayout(choice_layout)

        choice_label = QLabel("Choose an option:")
        choice_label.setAlignment(Qt.AlignCenter)
        choice_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        choice_layout.addWidget(choice_label)

        choice_desc = QLabel("Select 'Get Summary' to capture and summarize screen and audio content.\n"
                             "Select 'Ask Questions' to ask questions based on captured content.")
        choice_desc.setAlignment(Qt.AlignCenter)
        choice_desc.setWordWrap(True)
        choice_layout.addWidget(choice_desc)

        btn_summary = QPushButton("Get Summary")
        btn_summary.setFixedHeight(50)
        btn_summary.setToolTip("Capture screen and audio, then generate a summary.")
        btn_summary.clicked.connect(self.show_summary_view)
        choice_layout.addWidget(btn_summary)

        btn_qa = QPushButton("Ask Questions")
        btn_qa.setFixedHeight(50)
        btn_qa.setToolTip("Ask questions based on the captured content.")
        btn_qa.clicked.connect(self.show_qa_view)
        choice_layout.addWidget(btn_qa)

        self.stacked_widget.addWidget(choice_widget)

        # Summary view
        self.summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        self.summary_widget.setLayout(summary_layout)

        summary_instr = QLabel("Click 'Start Summary' to capture screen and audio, then generate and display a summary.")
        summary_instr.setWordWrap(True)
        summary_layout.addWidget(summary_instr)

        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.summary_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        summary_layout.addWidget(self.summary_box)

        self.start_btn = QPushButton("Start Summary")
        self.start_btn.setFixedHeight(40)
        self.start_btn.setToolTip("Start capturing and summarizing content.")
        self.start_btn.clicked.connect(self.run_summary_thread)
        summary_layout.addWidget(self.start_btn)

        self.back_btn_summary = QPushButton("Back")
        self.back_btn_summary.setFixedHeight(40)
        self.back_btn_summary.setToolTip("Return to the main menu.")
        self.back_btn_summary.clicked.connect(self.show_choice_view)
        summary_layout.addWidget(self.back_btn_summary)

        self.stacked_widget.addWidget(self.summary_widget)

        # QA view
        self.qa_widget = QWidget()
        qa_layout = QVBoxLayout()
        self.qa_widget.setLayout(qa_layout)

        qa_instr = QLabel("Enter a question related to the captured content and click 'Get Answer'.\n"
                          "The assistant answers questions based on the captured screen and audio content.")
        qa_instr.setWordWrap(True)
        qa_layout.addWidget(qa_instr)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("e.g., What are the key points from the meeting?")
        self.question_input.setFixedHeight(30)
        qa_layout.addWidget(self.question_input)

        self.ask_btn = QPushButton("Get Answer")
        self.ask_btn.setFixedHeight(40)
        self.ask_btn.setToolTip("Submit your question and get an answer based on captured content.")
        self.ask_btn.clicked.connect(self.run_qa_thread)
        qa_layout.addWidget(self.ask_btn)

        self.answer_box = QTextEdit()
        self.answer_box.setReadOnly(True)
        self.answer_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        qa_layout.addWidget(self.answer_box)

        self.back_btn_qa = QPushButton("Back")
        self.back_btn_qa.setFixedHeight(40)
        self.back_btn_qa.setToolTip("Return to the main menu.")
        self.back_btn_qa.clicked.connect(self.show_choice_view)
        qa_layout.addWidget(self.back_btn_qa)

        self.stacked_widget.addWidget(self.qa_widget)

        self.summary_ready.connect(self.update_summary)
        self.answer_ready.connect(self.update_answer)

        self.show_choice_view()

    def show_choice_view(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_summary_view(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_qa_view(self):
        self.stacked_widget.setCurrentIndex(2)

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
            # Capture screen and audio text on-demand
            screen_text = capture_text_once()
            audio_text = listen_and_transcribe()
            full_text = screen_text + " " + audio_text
            self.captured_text = full_text
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
