import time
import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab

# Set the tesseract executable path explicitly
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def capture_text_from_screenpipe():
    print("Starting screen capture and OCR...")
    captured_text = ""

    try:
        while True:
            # Grab the screen using PIL's ImageGrab
            screen = np.array(ImageGrab.grab())

            # Convert to grayscale for better OCR accuracy
            gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

            # Use pytesseract to do OCR on the captured image
            try:
                text = pytesseract.image_to_string(gray_screen)
            except pytesseract.TesseractError as e:
                print(f"Tesseract OCR error: {e}")
                text = ""

            if text:
                print(f"Captured text: {text}")
                captured_text += text + " "

            time.sleep(1)  # Adjust frequency as per your need
    except KeyboardInterrupt:
        print("Screen capture interrupted by user.")

    return captured_text
