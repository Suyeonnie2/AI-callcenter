from flask import Flask, jsonify, request,send_file, abort
from flask_cors import CORS
from controllers.conversation_controller import ConversationController
from services.conversation_service import AIConversationService
from controllers.speech_controller import SpeechController
from services.speech_service import SpeechService

app = Flask(__name__)
CORS(app)

ai_conversation_service = AIConversationService()
speech_service = SpeechService()
conversation_controller = ConversationController(ai_conversation_service, speech_service)
speech_controller = SpeechController(speech_service, ai_conversation_service)


@app.route('/start_conversation', methods=['GET'])
def start_conversation():
    return conversation_controller.start_conversation()

@app.route('/get_response', methods=['POST'])
def get_response():
    return conversation_controller.process_request()

# @app.route('/get_informative_response', methods=['POST'])
# def get_informative_response():
#     return conversation_controller.get_informative_response()

@app.route('/get_voice_response', methods=['POST'])
def get_voice_response():
    return speech_controller.get_voice_response()

@app.route('/audio/<path:filename>')
def get_audio(filename):
    try:
        return speech_controller.get_audio(filename)
    except FileNotFoundError:
        abort(404, description="Audio file not found")

if __name__ == '__main__':
    app.run(debug=True, port=5000)