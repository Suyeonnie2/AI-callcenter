from flask import jsonify, request, send_file
import os
from services.speech_service import SpeechService
from services.conversation_service import AIConversationService

class SpeechController:
        def __init__(self, speech_service: SpeechService, ai_conversation_service: AIConversationService):
            self.speech_service = speech_service
            self.conversation_service = ai_conversation_service

        def get_voice_response(self):
            user_input = self.speech_service.get_voice_input()
            response = self.ai_conversation_service.get_response(user_input)
            audio_file = self.speech_service.text_to_speech(response)
            
            return jsonify({
                "status": "success",
                "user_input": user_input,
                "message": response,
                "audio_file": os.path.basename(audio_file)
            }), 200

        def get_audio(self, filename):
            audio_dir = os.path.join(os.getcwd(), "audio_files")
            file_path = os.path.join(audio_dir, filename)
            if os.path.exists(file_path):
                return send_file(file_path, mimetype="audio/mp3")
            else:
                return jsonify({"error": "Audio file not found"}), 404