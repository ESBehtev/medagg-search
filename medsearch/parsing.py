import re
from typing import Dict, List
from .config_loader import load_taxonomy

_TAX = load_taxonomy()  # грузится 1 раз при импорте

def _match_labels(section, text: str) -> List[str]:
    labels = set()
    for item in section:
        if any(r.search(text) for r in item["patterns"]):
            labels.add(item["label"])
    return sorted(labels)

def extract_slots(query: str) -> Dict[str, List[str]]:
    text = query.lower()

    slots = {
        "modality": _match_labels(_TAX.modalities, text),
        "tasks":    _match_labels(_TAX.tasks, text),
        "organs":   _match_labels(_TAX.organs, text),
        "diseases": _match_labels(_TAX.diseases, text),
        "population": _match_labels(_TAX.population, text),
    }

    # ключевые слова (EN/RU/цифры), минус стоп-слова
    tokens = re.findall(r"[a-zа-яё0-9]+", text)
    keywords = [t for t in tokens if t not in _TAX.stopwords]

    return {**slots, "keywords": keywords}

def to_tag_query(slots: Dict[str, List[str]]) -> Dict[str, List[str]]:
    return {
        "modality": slots.get("modality", []),
        "organ": slots.get("organs", []),
        "disease": slots.get("diseases", []),
        "task": slots.get("tasks", []),
        "population": slots.get("population", []),
        "keywords": slots.get("keywords", []),
    }