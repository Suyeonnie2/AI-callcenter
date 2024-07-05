from flask import jsonify, request
from services.conversation_service import AIConversationService
from services.speech_service import SpeechService

import os

class ConversationController:
    def __init__(self, ai_conversation_service: AIConversationService, speech_service: SpeechService):
        self.ai_conversation_service = ai_conversation_service
        self.speech_service = speech_service

    def start_conversation(self):
        response = self.ai_conversation_service.start_conversation()
        audio_file = self.speech_service.text_to_speech(response)
        return jsonify({
            'status': 'success',
            'message': response,
            'audio_file': os.path.basename(audio_file)
        })

    def get_response(self):
        user_input = request.json['user_input']
        response = self.ai_conversation_service.get_response(user_input)
        audio_file = self.speech_service.text_to_speech(response)
        return jsonify({
            'status': 'success',
            'message': response,
            'audio_file': os.path.basename(audio_file)
        })
    
    def get_informaative_response(self):
        user_input = request.json.get('user_input')
        if not user_input:
            return jsonify({
                "status": "error",
                "message": "User input is required"
            }), 400
        
        response = self.ai_conversation_service.get_informative_response(user_input)
        return jsonify({
            "status": "success",
            "message": response
        }), 200
    
    def process_request(self):
        user_input = request.json['user_input']
        
        # 사용자 입력을 분석하여 적절한 응답 방식 결정
        if self.requires_company_info(user_input):
            response = self.ai_conversation_service.get_informative_response(user_input)
        else:
            response = self.ai_conversation_service.get_response(user_input)
        
        audio_file = self.speech_service.text_to_speech(response)
        return jsonify({
            'status': 'success',
            'message': response,
            'audio_file': os.path.basename(audio_file)
        })
    
    def requires_company_info(self, user_input):
        # 회사 정보 관련 키워드 목록
        company_info_keywords = ['회사', '정보', '연락처', '위치', '주소', '전화번호', '이메일']
        
        # 사용자 입력에 회사 정보 관련 키워드가 포함되어 있는지 확인
        return any(keyword in user_input for keyword in company_info_keywords)
