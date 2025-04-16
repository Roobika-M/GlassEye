import os
import time
import threading
from summarizer import summarize_text
from screen_capture import capture_screen
from audio_capture import capture_audio

DATA_DIR = os.path.expanduser("~/.screenpipe/data")
PROCESSED = set()

def run_screen_capture():
    capture_screen()

def run_audio_capture():
    capture_audio()

def watch_data_folder():
    print("\n📂 Watching for new data in:", DATA_DIR)
    while True:
        for file in os.listdir(DATA_DIR):
            filepath = os.path.join(DATA_DIR, file)
            if filepath in PROCESSED:
                continue

            if file.endswith(".txt") or file.endswith(".log"):  # You can tweak extensions here
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().strip()
                    if content:
                        print(f"\n📄 New file: {file}")
                        summary = summarize_text(content)
                        print(f"\n🧠 Summary:\n{summary}\n")
                        PROCESSED.add(filepath)
            elif file.endswith(".mp4"):
                # Optional: Transcribe mp4 to text first using Whisper or other tool
                pass

        time.sleep(5)  # Check every 5 seconds

def main():
    screen_thread = threading.Thread(target=run_screen_capture)
    audio_thread = threading.Thread(target=run_audio_capture)
    monitor_thread = threading.Thread(target=watch_data_folder)

    screen_thread.start()
    audio_thread.start()
    monitor_thread.start()

    screen_thread.join()
    audio_thread.join()
    monitor_thread.join()

if __name__ == "__main__":
    main()
