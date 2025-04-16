import time
import subprocess
import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab

# Function to run screenpipe and capture screen
def capture_screen():
    print("Screen recording and OCR capture is running...")

    # Start ScreenPipe to capture screen
    subprocess.run(["screenpipe", "--ocr-engine", "windows-native", "--fps", "1"])

    # Capture the screen every second
    while True:
        # Grab the screen using PIL's ImageGrab
        screen = np.array(ImageGrab.grab())

        # Convert to grayscale for better OCR accuracy
        gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

        # Use pytesseract to do OCR on the captured image
        text = pytesseract.image_to_string(gray_screen)

        if text:
            print(f"Captured text: {text}")

        time.sleep(1)  # Adjust frequency as per your need

# Run the capture function
if __name__ == "__main__":
    try:
        capture_screen()
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
