from typing import List
import re


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def simplify_text(text: str) -> str:
    # Very naive simplification: shorten long sentences and remove archaic terms
    replacements = {
        r"hereinafter": "from now on",
        r"aforesaid": "mentioned above",
        r"thereof": "of it",
        r"therein": "in it",
    }
    simple = text
    for pattern, repl in replacements.items():
        simple = re.sub(pattern, repl, simple, flags=re.IGNORECASE)

    sentences = split_sentences(simple)
    shortened = []
    for s in sentences:
        if len(s) > 240:
            # break with semicolons/commas if possible
            parts = re.split(r";|,", s)
            if len(parts) > 1:
                shortened.extend([p.strip() + "." for p in parts if p.strip()])
            else:
                shortened.append(s)
        else:
            shortened.append(s)

    return " " .join(shortened)

