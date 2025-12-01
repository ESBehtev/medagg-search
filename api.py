# medsearch/api.py
from __future__ import annotations

from typing import Dict, List, Tuple

# Новый импорт — берём полноценный объект парсинга
from .parsing import parse_query as parse_query_full, ParsedQuery


def parse_to_api(query: str) -> Dict[str, Dict]:
    """
    Новый высокоуровневый API:
    возвращает единый словарь:
    {
        "raw_query": "...",
        "slots": {...},
        "api_tags": {...}
    }
    Это основной интерфейс, который должен дергать бэкенд.
    """
    query = (query or "").strip()
    if not query:
        return {"raw_query": "", "slots": {}, "api_tags": {}}

    pq: ParsedQuery = parse_query_full(query)

    return {
        "raw_query": pq.raw_query,
        "slots": pq.slots,
        "api_tags": pq.api_tags,
    }


# -----------------------------
# Старый интерфейс (совместимость)
# -----------------------------

def parse_query(query: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Старый API, который возвращает (slots, tags).
    Используем для совместимости, но бэкенд должен переходить на parse_to_api.
    """
    query = (query or "").strip()
    if not query:
        return {}, {}

    pq: ParsedQuery = parse_query_full(query)
    return pq.slots, pq.api_tags


def parse_tags(query: str) -> Dict[str, List[str]]:
    """
    Упрощённый старый API: вернуть только tags.
    """
    _, tags = parse_query(query)
    return tags