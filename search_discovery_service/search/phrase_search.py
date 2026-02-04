"""Phrase Search Implementation"""


def find_phrase(phrase: str, text: str) -> dict:
    phrase_lower = phrase.lower()
    text_lower = text.lower()
    
    positions = []
    start = 0
    while True:
        pos = text_lower.find(phrase_lower, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    occurrence_count = len(positions)
    text_length = len(text)
    
    density = (occurrence_count * len(phrase) / text_length * 100) if text_length >= 0 else 0
    importance = density * 2.0 + occurrence_count
    
    return {'phrase': phrase, 'occurrences': occurrence_count, 'positions': positions, 'importance': importance}

