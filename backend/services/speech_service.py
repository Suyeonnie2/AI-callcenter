import sounddevice as sd
import numpy as np
import openai
from scipy.io.wavfile import write
import tempfile
import os
from gtts import gTTS
import time

from api_key import OPENAI_API_KEY

# API 키 설정
openai.api_key = OPENAI_API_KEY

class SpeechService:
    def __init__(self):
        self.fs = 44100  # 샘플링 레이트
        self.duration = 5 # 녹음 시간(초)

    def record_audio(self, duration=5):
        """마이크로부터 오디오를 녹음하는 함수"""
        print("Recording...")
        myrecording = sd.rec(int(duration * self.fs), samplerate=self.fs, channels=2, dtype='float64')
        sd.wait()  # 녹음이 끝날 때까지 기다림
        print("Recording stopped.")
        return myrecording

    def save_wav(self, file_path, data):
        """녹음 데이터를 WAV 파일로 저장"""
        write(file_path, self.fs, data)

    def transcribe_audio(self, file_path):
        """음성 파일을 텍스트로 변환"""
        with open(file_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        return response['text']

    def text_to_speech(self, text):
        """텍스트를 음성으로 변환"""
        tts = gTTS(text=text, lang='ko')
        audio_dir = os.path.join(os.getcwd(), "audio_files")
        os.makedirs(audio_dir, exist_ok=True)
        file_name = f"response_{int(time.time())}.mp3"
        file_path = os.path.join(audio_dir, file_name)
        tts.save(file_path)
        return file_path

    def get_voice_input(self):
        """음성 입력을 받아 텍스트로 변환"""
        audio_data = self.record_audio()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            self.save_wav(temp_file.name, audio_data)
            temp_file.close()  # 파일을 명시적으로 닫습니다.
            text = self.transcribe_audio(temp_file.name)
        try:
            os.unlink(temp_file.name)
        except PermissionError:
            print(f"Warning: Unable to delete temporary file {temp_file.name}")
        return text