import spacy

nlp = spacy.load('en_core_web_sm')

def extract_intent(text):   # app.py의 ask에서 들어온 내용을 인자로 넘김
    doc = nlp(text)
    intent = doc[0].text  # Assuming the first word represents the intent
    return intent