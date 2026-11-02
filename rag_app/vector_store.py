import json
from pathlib import Path

import numpy as np


def save_chunks(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def load_chunks(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    a = np.array(vector_a, dtype=float)
    b = np.array(vector_b, dtype=float)
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)


def search_similar_chunks(
    query_embedding: list[float], records: list[dict], top_k: int
) -> list[dict]:
    scored_records = []

    for record in records:
        score = cosine_similarity(query_embedding, record["embedding"])
        enriched = dict(record)
        enriched["score"] = score
        scored_records.append(enriched)

    scored_records.sort(key=lambda item: item["score"], reverse=True)
    return scored_records[:top_k]
