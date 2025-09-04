import spacy
from functools import lru_cache


@lru_cache(maxsize=1)
def get_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        # fallback to blank english if model not installed
        return spacy.blank("en")


def extract_locations(text: str):
    nlp = get_nlp()
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in {"GPE", "LOC"}]

