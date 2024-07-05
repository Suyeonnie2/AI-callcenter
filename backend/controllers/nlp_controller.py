from services.nlp_service import extract_intent

def process_text(text):
    intent = extract_intent(text)
    return intent