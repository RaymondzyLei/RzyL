import random
from datetime import datetime
from pathlib import Path


def load_random_sentence() -> str | None:
    try:
        sentences_file = Path(__file__).parent / "sentences.txt"
        with open(sentences_file, "r", encoding="utf-8") as f:
            sentences = f.readlines()
        if not sentences:
            return None
        while True:
            sentence = random.choice(sentences).strip()
            if sentence and not sentence.startswith("//"):
                return sentence
    except Exception:
        return None


def load_random_question() -> str | None:
    try:
        questions_file = Path(__file__).parent / "question.txt"
        with open(questions_file, "r", encoding="utf-8") as f:
            questions = f.readlines()
        if not questions:
            return None
        while True:
            question = random.choice(questions).strip()
            if question and not question.startswith("//"):
                return question
    except Exception:
        return None


def load_random_text() -> str | None:
    weekday = datetime.now().weekday()
    prob = 0.9 if weekday in (1, 4) else 0.4

    if random.random() < 0.3:
        sentence = load_random_sentence()
        if sentence:
            return f"\n{sentence}"
    elif random.random() < prob:
        question = load_random_question()
        if question:
            return f"\n{question}\n这是一个值得思考的问题😜"
    return None