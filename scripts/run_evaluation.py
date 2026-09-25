"""Run dense-only vs hybrid+RRF on the checked-in grounded dataset."""

import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from time import perf_counter

import numpy as np
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATASET = ROOT / "group_project" / "evaluation" / "golden_dataset.json"
OUTPUT = ROOT / "group_project" / "evaluation" / "evaluation_run.json"
CHECKPOINT = ROOT / "group_project" / "evaluation" / "evaluation_generations.json"
TOP_K = 5
EMBEDDING_MODEL = "text-embedding-3-small"
GENERATOR_MODEL = "gpt-4o-mini"


class ExactCosineCollection:
    """Chroma query-shaped adapter for exact cosine lookup on the real vectors."""

    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.vectors = np.asarray([chunk["embedding"] for chunk in chunks], dtype=np.float32)
        self.norms = np.linalg.norm(self.vectors, axis=1)

    def query(self, *, query_embeddings: list[list[float]], n_results: int, include: list[str]) -> dict:
        query = np.asarray(query_embeddings[0], dtype=np.float32)
        scores = np.clip(self.vectors @ query / (self.norms * np.linalg.norm(query)), -1, 1)
        indexes = np.argsort(-scores, kind="stable")[:n_results]
        selected = [self.chunks[int(index)] for index in indexes]
        return {
            "ids": [[chunk["id"] for chunk in selected]],
            "documents": [[chunk["content"] for chunk in selected]],
            "metadatas": [[chunk["metadata"] for chunk in selected]],
            "distances": [[float(1 - scores[index]) for index in indexes]],
        }


async def main() -> None:
    load_dotenv(ROOT / ".env")
    os.environ["EMBEDDING_PROVIDER"] = "openai"
    os.environ["EMBEDDING_MODEL"] = EMBEDDING_MODEL
    os.environ["LLM_PROVIDER"] = "openai"
    os.environ["LLM_MODEL"] = GENERATOR_MODEL

    from openai import AsyncOpenAI
    from ragas.embeddings.base import embedding_factory
    from ragas.llms import llm_factory
    from ragas.metrics.collections import (
        AnswerRelevancy,
        ContextPrecision,
        ContextRecall,
        Faithfulness,
    )

    from src import task10_generation as generation
    from src import task4_chunking_indexing as indexing
    from src import task5_semantic_search as semantic
    from src.task9_retrieval_pipeline import retrieve

    cases = json.loads(DATASET.read_text(encoding="utf-8"))
    if sys.argv[1:] == ["--score-only"]:
        saved = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        results = saved["rows"]
    else:
        chunks = indexing.chunk_documents(indexing.load_documents())
        embedded_chunks = indexing.embed_chunks(chunks)
        exact_collection = ExactCosineCollection(embedded_chunks)
        semantic.get_collection = lambda: exact_collection

        results = {}
        for name, retrieve_fn in (("dense-only", semantic.semantic_search), ("hybrid-rrf", retrieve)):
            generation.retrieve = retrieve_fn
            rows = []
            for index, case in enumerate(cases, 1):
                started = perf_counter()
                output = generation.generate_with_citation(case["question"], top_k=TOP_K)
                elapsed = perf_counter() - started
                sources = output["sources"]
                rows.append({
                    **case,
                    "response": output["answer"],
                    "retrieved_contexts": [item["content"] for item in sources],
                    "retrieved_sources": [item["metadata"]["source"] for item in sources],
                    "expected_source_hit": any(
                        item["metadata"]["source"] == case["expected_context"]
                        for item in sources
                    ),
                    "latency_seconds": elapsed,
                })
                print(f"{name}: generated {index}/{len(cases)}")
            results[name] = rows
        CHECKPOINT.write_text(json.dumps({"rows": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    client = AsyncOpenAI()
    evaluator_llm = llm_factory("gpt-4o-mini", client=client)
    evaluator_embeddings = embedding_factory(
        "openai", model=EMBEDDING_MODEL, client=client
    )
    metrics = {
        "faithfulness": Faithfulness(llm=evaluator_llm),
        "answer_relevancy": AnswerRelevancy(
            llm=evaluator_llm, embeddings=evaluator_embeddings
        ),
        "context_recall": ContextRecall(llm=evaluator_llm),
        "context_precision": ContextPrecision(llm=evaluator_llm),
    }
    semaphore = asyncio.Semaphore(4)

    async def score(row: dict) -> dict:
        async with semaphore:
            values = {}
            for name, metric in metrics.items():
                inputs = {"user_input": row["question"]}
                if name in {"faithfulness", "answer_relevancy"}:
                    inputs["response"] = row["response"]
                if name != "answer_relevancy":
                    inputs["retrieved_contexts"] = row["retrieved_contexts"]
                if name in {"context_recall", "context_precision"}:
                    inputs["reference"] = row["expected_answer"]
                result = await metric.ascore(**inputs)
                values[name] = float(result.value)
            return values

    summary = {}
    for name, rows in results.items():
        scores = await asyncio.gather(*(score(row) for row in rows))
        for row, score_row in zip(rows, scores):
            row["metrics"] = score_row
        summary[name] = {
            metric: mean(row["metrics"][metric] for row in rows)
            for metric in metrics
        }
        summary[name]["average"] = mean(summary[name].values())
        summary[name]["mean_latency_seconds"] = mean(row["latency_seconds"] for row in rows)
        summary[name]["expected_source_hit_at_5"] = mean(
            row["expected_source_hit"] for row in rows
        )

    payload = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_size": len(cases),
        "top_k": TOP_K,
        "embedding_model": EMBEDDING_MODEL,
        "generator_model": GENERATOR_MODEL,
        "evaluator_model": GENERATOR_MODEL,
        "retrieval_backend": "Exact cosine over real OpenAI embeddings; in-memory adapter (native Chroma upsert crashes on Windows)",
        "corpus_files": len(list((ROOT / "data" / "standardized").rglob("*.md"))),
        "summary": summary,
        "rows": results,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CHECKPOINT.unlink(missing_ok=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Saved raw per-question results to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(main())
