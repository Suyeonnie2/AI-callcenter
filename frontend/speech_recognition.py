import speech_recognition as sr

def recognize_speech(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text