from models.question import Question

# 가짜 데이터베이스 엔진
database = {
    "greeting": "Hello! How can I assist you today?",
    "farewell": "Goodbye! Have a great day!"
}

def query(intent):
    if intent in database:
        return database[intent]
    else:
        return "I'm sorry, I don't understand that question."