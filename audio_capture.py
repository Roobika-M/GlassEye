import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def listen_and_transcribe():
    recognized_text = ""
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            print("Listening for audio...")
            audio = recognizer.listen(source, timeout=5)
            # Recognize speech using Google Web Speech API
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized audio: {recognized_text}")
        except sr.UnknownValueError:
            print("Audio not recognized")
        except sr.RequestError:
            print("Error with the audio API")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")

    return recognized_text

# Run audio capture
if __name__ == "__main__":
    try:
        text = listen_and_transcribe()
        print(f"Transcribed text: {text}")
    except KeyboardInterrupt:
        print("Process interrupted by the user.")
