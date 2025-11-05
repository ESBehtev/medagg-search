import argparse, json
from .data import synthetic_datasets
from .scoring import HybridSearcher
from .parsing import to_tag_query

def main():
    parser = argparse.ArgumentParser(description="Medical dataset search (synthetic demo)")
    parser.add_argument("query", type=str, help="User query string")
    parser.add_argument("--k", type=int, default=5, help="Top-K results")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    datasets = synthetic_datasets()
    searcher = HybridSearcher(datasets)
    out = searcher.search(args.query, k=args.k)
    out["api_tags"] = to_tag_query(out["slots"])

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