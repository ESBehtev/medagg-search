# medsearch/api.py
from __future__ import annotations

from typing import Dict, List, Tuple

from .parsing import extract_slots, to_tag_query


def parse_query(query: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Высокоуровневый API для внешнего кода (Django-бэкенд, CLI и т.п.).

    На вход: строка запроса пользователя.
    На выход: (slots, tags), где:

      slots:
        {
          "modality": [...],
          "tasks": [...],
          "organs": [...],
          "diseases": [...],
          "population": [...],
          "keywords": [...]
        }

      tags:
        {
          "modality": [...],
          "organ": [...],
          "disease": [...],
          "task": [...],
          "population": [...],
          "keywords": [...]
        }

    Внутри:
      - regex-паттерны по таксономии,
      - Левенштейн для опечаток,
      - TF-IDF fallback для organs/diseases (если sklearn установлен).
    """
    query = (query or "").strip()
    if not query:
        return {}, {}

    slots = extract_slots(query)
    tags = to_tag_query(slots)
    return slots, tags


def parse_tags(query: str) -> Dict[str, List[str]]:
    """
    Упрощённый API: сразу вернуть только tags.
    Удобно для бэкенда, когда слоты "как есть" не нужны.
    """
    _, tags = parse_query(query)
    return tags