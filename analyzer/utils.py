import hashlib
from collections import Counter
import re

def sha256_hash(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def is_palindrome(value: str) -> bool:
    cleaned = value.lower()
    return cleaned == cleaned[::-1]

def word_count(value: str) -> int:
    return len(re.findall(r'\S+', value))

def character_frequency_map(value: str):
    return dict(Counter(value))

def compute_properties(value: str):
    return {
        "length": len(value),
        "is_palindrome": is_palindrome(value),
        "unique_characters": len(set(value)),
        "word_count": word_count(value),
        "sha256_hash": sha256_hash(value),
        "character_frequency_map": character_frequency_map(value),
    }
