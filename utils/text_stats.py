import re

def calculate_stats(text):

    words = text.split()
    text_for_sentences=re.sub(  r'\S+@\S+\.\S+', '', text)
    
    sentences = re.split(r"[.!?]+", text)
    sentences = re.split(
        r'[.!?]+',
        text_for_sentences
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    word_count = len(words)
    character_count = len(text)
    sentence_count = len(sentences)

    reading_time = max(1, round(word_count / 200))

    return {
        "words": word_count,
        "characters": character_count,
        "sentences": sentence_count,
        "reading_time": reading_time
    }