# validate.py
import requests
from rapidfuzz import fuzz

def validate_book(title, threshold=80):
    query = title.replace(" ", "+")
    url = f"https://openlibrary.org/search.json?title={query}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return False
        results = res.json().get("docs", [])
        for book in results[:5]:
            official = book.get("title")
            if official:
                score = fuzz.ratio(title.lower(), official.lower())
                if score >= threshold:
                    return True
    except Exception as e:
        print("Validation error:", e)
    return False
