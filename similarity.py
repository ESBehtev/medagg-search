# medsearch/similarity.py
from __future__ import annotations

from typing import Any, Iterable, List, Tuple

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _SKLEARN_AVAILABLE = True
except ImportError:  # graceful degradation
    TfidfVectorizer = None  # type: ignore
    cosine_similarity = None  # type: ignore
    _SKLEARN_AVAILABLE = False


def _item_label(item: Any) -> str:
    """Достаём label из объекта или dict'а."""
    if isinstance(item, dict):
        return str(item.get("label", "")).strip()
    return str(getattr(item, "label", "")).strip()


def _item_patterns(item: Any) -> Iterable[Any]:
    """Достаём patterns из объекта или dict'а."""
    if isinstance(item, dict):
        patterns = item.get("patterns", [])
    else:
        patterns = getattr(item, "patterns", [])
    if patterns is None:
        return []
    return patterns


class TaxonomyMatcher:
    """
    TF-IDF матчинг по секции таксономии (например diseases/organs).
    Используется как soft-fallback, когда regex/Левенштейн ничего не нашли.

    Если sklearn недоступен, просто всегда возвращает пустой список.
    """

    def __init__(self, section: Iterable[Any]) -> None:
        self._enabled = _SKLEARN_AVAILABLE
        self.labels: List[str] = []
        self._vectorizer = None
        self._X = None

        if not self._enabled:
            # sklearn нет — спокойно живём без TF-IDF
            return

        texts: List[str] = []

        for item in section:
            label = _item_label(item)
            if not label:
                continue
            patterns = list(_item_patterns(item))

            # Приводим паттерны к тексту
            pattern_texts: List[str] = []
            for p in patterns:
                # Если это re.Pattern
                pat_str = getattr(p, "pattern", None)
                if pat_str is None:
                    pat_str = str(p)
                pattern_texts.append(pat_str)

            # Документ: label + все паттерны
            doc = " ".join([label] + pattern_texts).lower()
            self.labels.append(label)
            texts.append(doc)

        if not texts:
            self._enabled = False
            return

        # char n-grams хорошо подходят для RU/EN и опечаток
        self._vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            min_df=1,
        )
        self._X = self._vectorizer.fit_transform(texts)

    def top_similar(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.3,
    ) -> List[Tuple[str, float]]:
        """
        Возвращает [(label, score), ...] с косинусной похожестью >= threshold,
        отсортированные по убыванию.
        """
        if not self._enabled:
            return []

        assert self._vectorizer is not None
        assert self._X is not None

        q = (query or "").strip().lower()
        if not q:
            return []

        q_vec = self._vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self._X)[0]
        idxs = sims.argsort()[::-1]

        results: List[Tuple[str, float]] = []
        for i in idxs:
            score = float(sims[i])
            if score < threshold:
                break
            label = self.labels[i]
            results.append((label, score))
            if len(results) >= top_k:
                break
        return results