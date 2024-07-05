import anthropic
from services.api_key import ANTHROPIC_API_KEY

class Completion:

    def __init__(self):
        print('init claude')
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # function to generate a chat completion
    def generate(self, user_prompt):
        messages = [
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.messages.create(
            system = "당신은 이제부터 AI 콜센터의 상담원입니다.",
            max_tokens = 4000,
            temperature= 0.0,
            model = "claude-3-opus-20240229",
            messages = messages
        )

        content = response.content[0].text

        return {
            "content": content
        }