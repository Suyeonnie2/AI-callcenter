# ai 상담원과 대화 서비스 로직

import csv
from utils import Completion
from data_loader import load_company_info, load_user_intent

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from translate import Translator

claude = Completion()

class AIConversationService:
    def __init__(self):
        # self.company_info = load_company_info('data/company_info.csv')
        self.user_intent = load_user_intent('data/user_intent.csv')
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        self.translator = Translator(from_lang="ko", to_lang="en")

        info_dict = load_company_info('data/company_info.csv')
        self.company_info = [f"{key}: {value}" for key, value in info_dict.items()]

        self.company_info_embeddings = self.model.encode(self.company_info)

    def get_response(self, user_input: str) -> str:
        return claude.generate(user_input)['content']

    def start_conversation(self) -> str:
        return "AI 상담원: 안녕하세요, 무엇을 도와드릴까요?"

    # def get_informative_response(self, user_input: str) -> str:
    #     intent = self.identify_intent(user_input)
        
    #     if intent == "company_info":
    #         key = self.extract_key(user_input)
    #         info = self.company_info.get(key, "해당 정보를 찾을 수 없습니다.")
    #         print("key: ", key)
    #         print("info: ", info)
            
    #         context = f"다음은 회사 정보입니다: {key} - {info}\n"
    #         instruction = (
    #             f"질문: {user_input}\n"
    #             "지침:\n"
    #             "1. 위의 회사 정보만을 사용하여 질문에 답하세요.\n"
    #             "2. 제공된 정보에 없는 내용은 '해당 정보가 없습니다'라고 답변하세요.\n"
    #             "3. 어떠한 경우에도 추측하거나 임의의 정보를 생성하지 마세요.\n"
    #             "답변:"
    #         )
                        
    #         full_prompt = context + instruction
    #         ai_response = claude.generate(full_prompt)['content']
    #         # ai_response = self.verify_response(ai_response, info)
            
    #         return f"AI 상담원: {ai_response}"
        
    #     return f"AI 상담원: {self.user_intent.get(intent, '문의하신 내용에 대한 답변을 찾을 수 없습니다.')}"

    def prepare_company_info(self):
        return [f"{key}: {value}" for key, value in self.company_info.items()]
    
    def translate_to_english(self, text):
        return self.translator.translate(text)

    def get_informative_response(self, user_input: str) -> str:
            
            user_input = self.translate_to_english(user_input)
            print(user_input)

            question_embedding = self.model.encode([user_input])
            similarities = cosine_similarity(question_embedding, self.company_info_embeddings)[0]
            most_relevant_idx = np.argmax(similarities)

            print(self.company_info)

            print(most_relevant_idx)
            
            context = f"관련 회사 정보: {self.company_info[most_relevant_idx]}\n"
            instruction = (f"질문: {user_input}\n"
                "지침:\n"
                "1. 위의 회사 정보만을 사용하여 질문에 답하세요.\n"
                "2. 제공된 정보에 없는 내용은 '해당 정보가 없습니다'라고 답변하세요.\n"
                "3. 어떠한 경우에도 추측하거나 임의의 정보를 생성하지 마세요.\n"
                "답변:")
            
            full_prompt = context + instruction
            ai_response = claude.generate(full_prompt)['content']
            
            return f"AI 상담원: {ai_response}"
        
    
    def verify_response(self, response, provided_info):
        # 간단한 검증: 응답에 제공된 정보의 키워드가 포함되어 있는지 확인
        keywords = provided_info.lower().split()
        response_lower = response.lower()
        if not any(keyword in response_lower for keyword in keywords):
            return "죄송합니다. 제공된 정보로 답변할 수 없습니다."
        return response

    def identify_intent(self, user_input: str) -> str:
        if "회사 정보" in user_input or "연락처" in user_input or "위치" in user_input:
            return "company_info"
        elif "문의" in user_input:
            return "inquiry"
        else:
            return None

    def extract_key(self, user_input: str) -> str:
        if "회사" in user_input:
            return "company_overview"
        if "연락처" in user_input:
            return "contact_info"
        if "위치" in user_input:
            return "location"
        return ""