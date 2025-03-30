# extract.py
import re
import spacy
from spacy.cli import download

#python -m spacy download en_core_web_sm
download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")

def extract_books_from_comment(text):
    candidates = []

    # Rule 1: Quoted or italicized
    quoted = re.findall(r'"(.*?)"|“(.*?)”|\*(.*?)\*', text)
    for group in quoted:
        for match in group:
            if match.strip():
                candidates.append(match.strip())

    # Rule 2: "by" pattern
    by_pattern = re.findall(r"(.*?)\s+by\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?", text)
    for match in by_pattern:
        candidates.append(match.strip())

    # Rule 3: Named entities
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":
            candidates.append(ent.text.strip())

    return list(set(candidates))
