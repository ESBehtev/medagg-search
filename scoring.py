from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .data import DatasetCard
from .parsing import extract_slots

def _build_corpus(datasets: List[DatasetCard]) -> List[str]:
    texts = []
    for d in datasets:
        block = " ".join([
            d.title, d.abstract,
            " ".join(d.modality), " ".join(d.organs),
            " ".join(d.diseases), " ".join(d.tasks),
            " ".join(d.population)
        ])
        texts.append(block.lower())
    return texts

class HybridSearcher:
    def __init__(self, datasets: List[DatasetCard]):
        self.datasets = datasets
        self.corpus = _build_corpus(datasets)
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1)
        self.X = self.vectorizer.fit_transform(self.corpus)

    def _slot_bonus(self, slots: Dict[str, List[str]], d: DatasetCard) -> float:
        bonus = 0.0
        if slots["modality"]:
            bonus += 0.5 * len(set(slots["modality"]) & set([m.lower() for m in d.modality]))
        if slots["organs"]:
            bonus += 0.4 * len(set(slots["organs"]) & set([o.lower() for o in d.organs]))
        if slots["diseases"]:
            bonus += 0.6 * len(set(slots["diseases"]) & set([di.lower() for di in d.diseases]))
        if slots["tasks"]:
            bonus += 0.5 * len(set(slots["tasks"]) & set([t.lower() for t in d.tasks]))
        if slots["population"]:
            bonus += 0.2 * len(set(slots["population"]) & set([p.lower() for p in d.population]))
        bonus += 0.3 * ((getattr(d, "year", 2020) - 2017)/10.0)
        return bonus

    def search(self, query: str, k: int = 5):
        slots = extract_slots(query)
        q = " ".join(slots["keywords"] + slots["modality"] + slots["organs"] + slots["diseases"] + slots["tasks"])
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.X)[0]
        sims = (sims - sims.mean()) / (sims.std() + 1e-6)

        scores = []
        for i, d in enumerate(self.datasets):
            s = float(sims[i]) + self._slot_bonus(slots, d)
            scores.append(s)

        order = np.argsort(scores)[::-1][:k]
        results = []
        for rank, idx in enumerate(order, start=1):
            d = self.datasets[idx]
            results.append({
                "rank": rank,
                "score": round(float(scores[idx]), 4),
                "id": d.id,
                "title": d.title,
                "year": d.year,
                "link": d.link,
                "modality": d.modality,
                "organs": d.organs,
                "diseases": d.diseases,
                "tasks": d.tasks,
                "population": d.population,
            })
        return {"slots": slots, "results": results}