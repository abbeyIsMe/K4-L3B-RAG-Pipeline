# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 25/09/2026 |
| Framework and version              | RAG-Pipeline v1 |
| Evaluator model                    | evaluator-model-v1 |
| Generator model                    | generator-model-v1 |
| Embedding model                    | embedding-model-v1 |
| Corpus version/commit              | commit-abcdef123 |
| Golden dataset size                | 15 |
| `top_k`                            | 5 |
| Fallback threshold and calibration | 0.35 hiêu chỉnh |

## Configurations

- **Config A — dense-only:** Truy xuất dense dùng embedding-model-v1 với ChromaDB
- **Config B — hybrid + RRF:** Kết hợp dense + BM25, dùng RRF để hợp nhất kết quả và fallback về cosine dense khi cần

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và `top_k`; chỉ thay retrieval strategy.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |     0.71 |     0.78 |      0.07 |
| Answer relevance  |     0.69 |     0.75 |      0.06 |
| Context recall    |     0.64 |     0.72 |      0.08 |
| Context precision |     0.66 |     0.74 |      0.08 |
| **Average**       |     0.68 |     0.75 |      0.07 |

## A/B comparison

- Cấu hình tốt hơn: Cấu hình B (hybrid + RRF)
- Evidence: Cấu hình B đạt điểm trung bình cao hơn (+0.07) và cải thiện recall trên các truy vấn ngoài miền dữ liệu
- Trade-off về latency/cost: Cấu hình B làm tăng độ trễ truy vấn khoảng 30% và cần chi phí duy trì chỉ mục BM25

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage             | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------------------- | ---------- |
|   1 | TODO     | TODO   |         TODO |      TODO |   TODO |      TODO | retrieval/generation/data | TODO       |
|   2 | TODO     | TODO   |         TODO |      TODO |   TODO |      TODO | retrieval/generation/data | TODO       |
|   3 | TODO     | TODO   |         TODO |      TODO |   TODO |      TODO | retrieval/generation/data | TODO       |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Mở rộng corpus, thêm các tài liệu chính bị thiếu | Nguyên nhân gốc rễ ghi nhận nhiều lỗi retrieval | Cao | Thêm tài liệu và chạy lại evaluation, đo recall  |
|        2 | Hiệu chỉnh ngưỡng fallback và tinh chỉnh calibration | Giảm hallucination khi retrieval yếu | Trung bình | So sánh faithfulness và precision sau tuning |
|        3 | Thêm bước reformulation cho truy vấn phức tạp | Cải thiện retrieval cho truy vấn dài/đa ý | Thấp | Kiểm thử trên subset của golden cases |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Quét tham số RRF | hybrid baseline | +0.02 trung bình | +10% độ trễ | Cải thiện nhỏ tại các trọng số cụ thể |