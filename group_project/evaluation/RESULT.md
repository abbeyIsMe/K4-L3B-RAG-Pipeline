# RAG evaluation results

## Run information

| Field | Value |
|---|---|
| Evaluation date | 25/09/2026 |
| Framework | RAGAS 0.4.3 |
| Generator and evaluator | `gpt-4o-mini` |
| Embedding | `text-embedding-3-small` (1536 dimensions) |
| Corpus | 10 standardized documents, 329 chunks, local working tree on 25/09/2026 |
| Golden dataset | 15 grounded HUTECH admissions questions |
| `top_k` | 5 |
| Fallback threshold | 0.3 (existing setting; not tuned in this run) |
| Retrieval scoring | Exact cosine over real OpenAI embeddings, in-memory evaluation adapter |

## Configurations

- **Config A — dense-only:** exact cosine dense retrieval.
- **Config B — hybrid + RRF:** exact cosine dense retrieval plus the project's BM25 lexical retrieval and RRF fusion, followed by the existing fallback/generation path.

Both configurations used the same questions, generator, evaluator, embedding model, prompt and `top_k`. Chroma's native HNSW upsert crashed in this Windows/Python environment, so evaluation used exact cosine against the actual OpenAI embeddings and corpus chunks. The run does not measure persisted Chroma/HNSW behavior or its approximate-neighbor latency. Raw per-question outputs and metric values are in `evaluation_run.json`.

## Overall scores

RAGAS scores are on a 0–1 scale. “Average” is the unweighted mean of the four metrics.

| Metric | Config A | Config B | Delta B−A |
|---|---:|---:|---:|
| Faithfulness | 0.8357 | 0.9794 | +0.1437 |
| Answer relevance | 0.4281 | 0.5454 | +0.1173 |
| Context recall | 0.6667 | 0.8333 | +0.1667 |
| Context precision | 0.5863 | 0.7419 | +0.1556 |
| **Average** | **0.6292** | **0.7750** | **+0.1458** |

| Operational measure | Config A | Config B |
|---|---:|---:|
| Mean end-to-end generation latency | 6.18 s | 7.59 s |
| Expected source hit@5 (file-level) | 80.0% (12/15) | 93.3% (14/15) |

Latency includes query embedding and answer generation, but excludes RAGAS scoring. File-level hit@5 only checks whether the expected source file appears; it does not establish that the exact answer-bearing passage was retrieved.

## A/B comparison

Hybrid + RRF scored 0.1458 higher on the unweighted average and improved each reported RAGAS metric. Its mean latency was 1.41 seconds (22.9%) higher. These are results from this 15-question set and exact-cosine adapter; they do not establish statistical significance or native Chroma performance.

## Worst performers

| Question | Config | Faithfulness | Relevance | Recall | Precision | Observed failure |
|---|---|---:|---:|---:|---:|---|
| What is the planned 2026 HUTECH Medicine enrollment quota? | A and B | 1.0000 | 0.0000 | 0.0000 | 0.0000 | Safe refusal; expected legal source is present among retrieved files in B, but the answer-bearing passage was not sufficient to answer. |
| How much is HUTECH Medicine tuition per payment period in 2026? | A and B | 1.0000 | 0.0000 | 0.0000 | 0.0000 | Safe refusal; expected source file was absent from top 5 in B. |
| How many tuition installments does HUTECH collect each year? | A | 1.0000 | 0.0000 | 0.0000 | 0.0000 | Dense-only refused despite the expected source file appearing in retrieved files; B answered this case. |

The full raw outputs are retained in `evaluation_run.json`. A file-level source hit can coexist with a failed answer when the retrieved chunk does not contain the needed fact.

## Recommendations

| Priority | Action | Evidence | Verification |
|---:|---|---|---|
| 1 | Improve retrieval of answer-bearing passages for quota and Medicine tuition facts. | Both configurations scored zero for relevance, recall and precision on the Medicine tuition question; the quota question also had zero relevance/recall/precision. | Inspect retrieved chunk IDs and source sections, revise chunk boundaries or lexical terms, then rerun the same 15 cases and compare per-question context recall. |
| 2 | Re-run against native Chroma after resolving the Windows HNSW crash. | This run used exact cosine and an in-memory adapter, not persisted Chroma. | Build/query the Chroma collection and compare top-5 IDs, latency and all four metrics on the same dataset. |
| 3 | Review answer support on scholarship edge cases. | Hybrid faithfulness was 0.8333 for the healthcare employees' children scholarship question and 0.8571 for the talent scholarship eligibility/value question. | Compare each generated claim to its retrieved passages and rerun after prompt or retrieval changes. |

## Additional experiments

No RRF parameter sweep or threshold calibration was run; the existing fallback threshold remained 0.3. No results are reported for those experiments.
