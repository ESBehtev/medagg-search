# medsearch/parsing.py
from __future__ import annotations

import re
from typing import Dict, List

from .config_loader import load_taxonomy
from .similarity import TaxonomyMatcher

_TAX = load_taxonomy()  # грузится 1 раз при импорте

# Инициализируем TF-IDF матчеры для soft-fallback
_DISEASE_MATCHER = TaxonomyMatcher(_TAX.diseases)
_ORGAN_MATCHER = TaxonomyMatcher(_TAX.organs)



def _levenshtein(a: str, b: str) -> int:
    """
    Простая реализация расстояния Левенштейна для небольших слов.
    Используется только для матчей токенов на label (опечатки).
    """
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


def _match_labels_regex(section, text: str) -> List[str]:
    """
    Строгий матч: пробегаем по паттернам из таксономии и ищем regex-срабатывания.
    """
    labels = set()
    for item in section:
        patterns = getattr(item, "patterns", None) or item["patterns"]
        for r in patterns:
            # r может быть re.Pattern или строкой
            if hasattr(r, "search"):
                if r.search(text):
                    labels.add(getattr(item, "label", item["label"]))
                    break
            else:
                # на всякий случай, если не скомпилировали
                if re.search(str(r), text):
                    labels.add(getattr(item, "label", item["label"]))
                    break
    return sorted(labels)


def _match_labels_fuzzy(section, tokens: List[str], max_distance: int = 1) -> List[str]:
    """
    Фуззи-матч по Левенштейну: если токен отличается от label не более чем
    на max_distance символов, считаем совпадением (для опечаток).
    """
    labels = set()

    for item in section:
        label = getattr(item, "label", item["label"])
        base = str(label).lower()

        for t in tokens:
            if _levenshtein(t, base) <= max_distance:
                labels.add(label)
                break

    return sorted(labels)


def extract_slots(query: str) -> Dict[str, List[str]]:
    """
    Основной парсер:

    1. Нормализуем текст.
    2. Выделяем слоты через regex-паттерны.
    3. Добавляем фуззи-совпадения по Левенштейну (опечатки).
    4. Если после этого disease/organ пустые — пробуем TF-IDF fallback.
    5. Выделяем keywords (токены без стоп-слов).
    """
    text = (query or "").lower()
    tokens = re.findall(r"[a-zа-яё0-9]+", text)

    # 1) жёсткий regex-матч
    slots = {
        "modality": _match_labels_regex(_TAX.modalities, text),
        "tasks": _match_labels_regex(_TAX.tasks, text),
        "organs": _match_labels_regex(_TAX.organs, text),
        "diseases": _match_labels_regex(_TAX.diseases, text),
        "population": _match_labels_regex(_TAX.population, text),
    }

    # 2) Левенштейн для опечаток (добавляем поверх regex-результата)
    slots["modality"] = sorted(
        set(slots["modality"]) |
        set(_match_labels_fuzzy(_TAX.modalities, tokens))
    )
    slots["tasks"] = sorted(
        set(slots["tasks"]) |
        set(_match_labels_fuzzy(_TAX.tasks, tokens))
    )
    slots["organs"] = sorted(
        set(slots["organs"]) |
        set(_match_labels_fuzzy(_TAX.organs, tokens))
    )
    slots["diseases"] = sorted(
        set(slots["diseases"]) |
        set(_match_labels_fuzzy(_TAX.diseases, tokens))
    )
    slots["population"] = sorted(
        set(slots["population"]) |
        set(_match_labels_fuzzy(_TAX.population, tokens))
    )

    # 3) TF-IDF fallback для органов / заболеваний:
    # если после regex+Левенштейна disease/organ пустые, пробуем подобрать похожее.
    if not slots["diseases"]:
        tfidf_diseases = _DISEASE_MATCHER.top_similar(query, top_k=2, threshold=0.35)
        slots["diseases"] = sorted({label for label, score in tfidf_diseases})

    if not slots["organs"]:
        tfidf_organs = _ORGAN_MATCHER.top_similar(query, top_k=1, threshold=0.45)
        slots["organs"] = sorted({label for label, score in tfidf_organs})

    if "ECG" in slots["modality"] and not slots["organs"]:
        slots["organs"] = ["heart"]
        
    # 4) ключевые слова (EN/RU/цифры), минус стоп-слова
    stopwords = getattr(_TAX, "stopwords", None) or _TAX.stopwords
    keywords = [t for t in tokens if t not in stopwords]

    return {**slots, "keywords": keywords}


def to_tag_query(slots: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Приводим внутренние слоты к API-формату тегов.
    """
    return {
        "modality": slots.get("modality", []),
        "organ": slots.get("organs", []),
        "disease": slots.get("diseases", []),
        "task": slots.get("tasks", []),
        "population": slots.get("population", []),
        "keywords": slots.get("keywords", []),
    }