from __future__ import annotations
import re, pathlib, yaml
from typing import Dict, List, Any

DEFAULT_PATH = pathlib.Path(__file__).with_suffix("") / "taxonomy.yaml"

class CompiledTaxonomy:
    def __init__(self, raw: Dict[str, Any]):
        self.stopwords: set[str] = set(raw.get("stopwords", []))
        self.modalities = self._compile_section(raw.get("modalities", []))
        self.tasks     = self._compile_section(raw.get("tasks", []))
        self.organs    = self._compile_section(raw.get("organs", []))
        self.diseases  = self._compile_section(raw.get("diseases", []))
        self.population= self._compile_section(raw.get("population", []))

    @staticmethod
    def _compile_section(items: List[Dict[str, Any]]):
        compiled = []
        for it in items:
            label = it["label"]
            pats = it.get("patterns", [])
            regexes = [re.compile(p, flags=re.IGNORECASE) for p in pats]
            compiled.append({"label": label, "patterns": regexes})
        return compiled

def load_taxonomy(path: str | None = None) -> CompiledTaxonomy:
    p = pathlib.Path(path) if path else DEFAULT_PATH
    with open(p, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return CompiledTaxonomy(raw)