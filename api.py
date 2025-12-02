# medsearch/api.py
from __future__ import annotations

from typing import Dict, List, Tuple

# Универсальный импорт
try:
    from .parsing import parse_query as parse_query_full, ParsedQuery
except ImportError:
    from parsing import parse_query as parse_query_full, ParsedQuery


def parse_to_api(query: str) -> Dict:
    query = (query or "").strip()
    if not query:
        return {"raw_query": "", "slots": {}, "api_tags": {}}

    pq: ParsedQuery = parse_query_full(query)

    return {
        "raw_query": pq.raw_query,
        "slots": pq.slots,
        "api_tags": pq.api_tags,
    }


# Старые интерфейсы (чтобы ничего не ломать в бэкенде)

def parse_query(query: str):
    query = (query or "").strip()
    if not query:
        return {}, {}
    pq: ParsedQuery = parse_query_full(query)
    return pq.slots, pq.api_tags


def parse_tags(query: str):
    _, tags = parse_query(query)
    return tags