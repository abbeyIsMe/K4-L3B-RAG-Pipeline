# Báo cáo đóng góp cá nhân

## Thông tin

<<<<<<< Updated upstream
- Họ và tên:
- Mã học viên:
- Nhóm:
- Repository/branch:
=======
- Họ và tên: Hồ Hoàng Phương Anh
- Mã học viên: 2A202602460
- Nhóm: Hello Data
- Repository/branch: https://github.com/abbeyIsMe/K4-L3B-RAG-Pipeline
>>>>>>> Stashed changes

## Phần việc đã thực hiện

| Module / deliverable | Việc tôi trực tiếp làm | File / commit / PR | Trạng thái |
| --- | --- | --- | --- |
| Chọn chủ đề và scope sản phẩm, phân công công viẹc | Xác định chủ đề tối ưu cho nhóm là tuyển sinh, đồng thời xác lập phạm vi dữ liệu, câu hỏi mẫu và mục tiêu output của chatbot. | `group_project/evaluation/golden_dataset.json`, `RESULT.md`, `TEAMMATES.md` | Done |
| Thiết kế golden dataset | Soạn 15 câu hỏi tuyển sinh theo format `question`, `expected_answer`, `expected_context` để làm cơ sở đánh giá chất lượng | `group_project/evaluation/golden_dataset.json` | Done |
| Viết báo cáo đánh giá | Hoàn thiện nội dung báo cáo kết quả đánh giá A/B, kết luận và khuyến nghị cho hệ thống. | `group_project/evaluation/RESULT.md` | Done |
| Chuẩn hóa tài liệu cá nhân | Điền template báo cáo cá nhân, mô tả phần việc, bằng chứng và tiến độ kiểm thử. | `reports/INDIVIDUAL_REPORT.md` | Done |

Những phần việc trên đều có thể đối chiếu bằng file báo cáo và file dữ liệu trong repository, phù hợp với mục đích đánh giá cá nhân trong lab.

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chọn chủ đề tuyển sinh cho sản phẩm RAG.
   - **Lý do/evidence:** Chủ đề này có dữ liệu dễ thu thập, nội dung mang tính chính thống, và phù hợp với yêu cầu “hỏi đáp theo chính sách, quy trình, thông tin tuyển sinh”.
   - **Trade-off:** Đòi hỏi nội dung QA phải rõ ràng và định hình dữ liệu theo domain cụ thể; tuy nhiên, nhược điểm này được bù bằng tính dễ đo lường và dễ tạo golden dataset.

<<<<<<< Updated upstream
1. **Quyết định:**  
   **Lý do/evidence:**  
   **Trade-off:**

2. **Quyết định:**  
   **Lý do/evidence:**  
   **Trade-off:**
=======
2. **Quyết định:** Dùng golden dataset theo topic tuyển sinh để kiểm tra chất lượng hệ thống.
   - **Lý do/evidence:** Golden dataset giúp đánh giá chatbot một cách có hệ thống, dễ so sánh hai cấu hình retrieval (dense-only vs hybrid + RRF) và theo dõi các lỗi chính như thiếu context, hallucination.
   - **Trade-off:** Chi phí thiết kế dataset lớn hơn, nhưng hiệu quả trong việc đánh giá và báo cáo cao hơn nhiều so với chỉ chạy thử dùm.
>>>>>>> Stashed changes

## Kiểm thử và kết quả

- Test hoặc query đã dùng:
  - `pytest tests/test_acceptance.py -q`
  - `pytest tests/test_contracts.py -q`
  - `pytest -q`
- Kết quả chính:
  - Acceptance tests đã đạt trạng thái pass về nội dung dữ liệu, golden set và report yêu cầu.
  - Các contract tests cần kiểm tra đồng bộ dependencies / môi trường Python, đặc biệt các package như `langchain_text_splitters` và `rank_bm25`.
- Lỗi đã phát hiện và cách xử lý:
  - Tìm thấy lỗi thiếu dependency khi chạy pymodule retrieval và BM25.
  - Cách xử lý: cài đặt lại môi trường dev theo hướng dẫn dự án và chạy pytest lại để kiểm tra cuối cùng.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: golden dataset và báo cáo hiện mới tập trung trên chủ đề tuyển sinh, nên cần bổ sung thêm dữ liệu thực tế và kiểm tra độ phủ cho các edge cases hơn.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: bổ sung thêm dữ liệu đào tạo và mở rộng golden set theo nhiều nhánh vấn đề khác nhau như quy trình, học bổng, thời hạn, hồ sơ, xét tuyển thẳng.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

<<<<<<< Updated upstream
- Ngày:
- Tên thành viên:
=======
- Ngày: 25/09/2026
- Tên thành viên: Hồ Hoàng Phương Anh
>>>>>>> Stashed changes
