import argparse
import json

from .data import synthetic_datasets
from .parsing import to_tag_query
from .scoring import HybridSearcher


def search(query, k):
    """Search function that can be called from other Python code"""
    datasets = synthetic_datasets()
    searcher = HybridSearcher(datasets)

    result = searcher.search(query, k)
    result["api_tags"] = to_tag_query(result["slots"])

    return result

def main():
    parser = argparse.ArgumentParser(description="Medical dataset search (synthetic demo)")
    parser.add_argument("query", type=str, help="User query string")
    parser.add_argument("--k", type=int, default=5, help="Top-K results")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    out = search(args.query, k=args.k)

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("Parsed slots:", out["slots"])
        print("API tags:", out["api_tags"])
        print(f"\nTop-{args.k} results:")
        for r in out["results"]:
            print(f"[{r['rank']}] {r['title']} (score={r['score']}, year={r['year']}) -> {r['link']}")
            print(f"    modality={r['modality']} | organs={r['organs']} | diseases={r['diseases']} | tasks={r['tasks']} | pop={r['population']}")

if __name__ == "__main__":
    main()
