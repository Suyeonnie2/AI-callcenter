def extract_intent(text):
    # 간단히 첫 단어를 의도로 사용하는 예시 코드입니다.
    words = text.split()
    intent = words[0] if words else None
    return intent