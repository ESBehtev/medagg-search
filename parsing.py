# medsearch/parsing.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Any

# --- Универсальные импорты (работают и как пакет, и как скрипт) ---
try:
    from .config_loader import load_taxonomy
    from .similarity import TaxonomyMatcher
except ImportError:
    from config_loader import load_taxonomy
    from similarity import TaxonomyMatcher


@dataclass
class ParsedQuery:
    raw_query: str
    slots: Dict[str, List[str]]
    api_tags: Dict[str, Any]


_TAX = load_taxonomy()

_DISEASE_MATCHER = TaxonomyMatcher(_TAX.diseases)
_ORGAN_MATCHER = TaxonomyMatcher(_TAX.organs)


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev_row = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur_row = [i]
        for j, cb in enumerate(b, start=1):
            insert_cost = cur_row[j - 1] + 1
            delete_cost = prev_row[j] + 1
            replace_cost = prev_row[j - 1] + (ca != cb)
            cur_row.append(min(insert_cost, delete_cost, replace_cost))
        prev_row = cur_row
    return prev_row[-1]


def _match_labels_regex(section, text: str):
    labels = set()
    for item in section:
        patterns = getattr(item, "patterns", None) or item["patterns"]
        for r in patterns:
            if hasattr(r, "search"):
                if r.search(text):
                    labels.add(getattr(item, "label", item["label"]))
                    break
            else:
                if re.search(str(r), text):
                    labels.add(getattr(item, "label", item["label"]))
                    break
    return sorted(labels)


def _match_labels_fuzzy(section, tokens, max_distance=1):
    labels = set()
    for item in section:
        label = getattr(item, "label", item["label"])
        base = label.lower()
        for t in tokens:
            if _levenshtein(t, base) <= max_distance:
                labels.add(label)
                break
    return sorted(labels)


def extract_slots(query: str) -> Dict[str, List[str]]:
    text = (query or "").lower()
    tokens = re.findall(r"[a-zа-яё0-9]+", text)

    slots = {
        "modality": _match_labels_regex(_TAX.modalities, text),
        "tasks": _match_labels_regex(_TAX.tasks, text),
        "organs": _match_labels_regex(_TAX.organs, text),
        "diseases": _match_labels_regex(_TAX.diseases, text),
        "population": _match_labels_regex(_TAX.population, text),
    }

    slots["modality"] = sorted(set(slots["modality"]) | set(_match_labels_fuzzy(_TAX.modalities, tokens)))
    slots["tasks"] = sorted(set(slots["tasks"]) | set(_match_labels_fuzzy(_TAX.tasks, tokens)))
    slots["organs"] = sorted(set(slots["organs"]) | set(_match_labels_fuzzy(_TAX.organs, tokens)))
    slots["diseases"] = sorted(set(slots["diseases"]) | set(_match_labels_fuzzy(_TAX.diseases, tokens)))
    slots["population"] = sorted(set(slots["population"]) | set(_match_labels_fuzzy(_TAX.population, tokens)))

    if not slots["diseases"]:
        tfidf = _DISEASE_MATCHER.top_similar(query, top_k=2, threshold=0.35)
        slots["diseases"] = sorted({lbl for lbl, score in tfidf})

    if not slots["organs"]:
        tfidf = _ORGAN_MATCHER.top_similar(query, top_k=1, threshold=0.45)
        slots["organs"] = sorted({lbl for lbl, score in tfidf})

    if "ECG" in slots["modality"] and not slots["organs"]:
        slots["organs"] = ["heart"]

    stopwords = getattr(_TAX, "stopwords", None) or _TAX.stopwords
    tokens_clean = [t for t in tokens if t not in stopwords]

    return {**slots, "keywords": tokens_clean}


def to_tag_query(slots):
    return {
        "modality": slots.get("modality", []),
        "organ": slots.get("organs", []),
        "disease": slots.get("diseases", []),
        "task": slots.get("tasks", []),
        "population": slots.get("population", []),
        "keywords": slots.get("keywords", []),
    }


def parse_query(raw_query: str) -> ParsedQuery:
    slots = extract_slots(raw_query)
    api_tags = to_tag_query(slots)
    return ParsedQuery(raw_query=raw_query, slots=slots, api_tags=api_tags)