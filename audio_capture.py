import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def capture_audio():
    # Initialize microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("Listening for audio...")
            audio = recognizer.listen(source)
            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio)
                print(f"Recognized audio: {text}")
            except sr.UnknownValueError:
                print("Audio not recognized")
            except sr.RequestError:
                print("Error with the audio API")

# Run audio capture
if __name__ == "__main__":
    try:
        capture_audio()
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
