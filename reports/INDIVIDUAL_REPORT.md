# Individual Contribution Report

## Thông tin

- **Họ và tên:** Đoàn Phương Linh
- **Mã học viên:** 2A202602382
- **Nhóm:** Hello World
- **Repository/branch:** https://github.com/abbeyIsMe/K4-L3B-RAG-Pipeline

---

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Thu thập dữ liệu (Crawl Data) | Crawl và chuẩn hóa tài liệu tuyển sinh HUTECH 2026 (học bổng, phương thức tuyển sinh, chương trình đào tạo) từ nguồn chính thức; chuyển PDF sang Markdown chuẩn hóa để pipeline có thể ingest | `data/landing/legal/hutech_2026_hoc_bong.pdf`, `data/landing/legal/hutech_2026_phuong_thuc_tuyen_sinh.pdf`, `data/landing/legal/hutech_2026_chuong_trinh_dao_tao.pdf`, `data/standardized/legal/*.md` | Done |
| Sinh snapshot chính thức | Viết script sinh snapshot Markdown chính thức từ dữ liệu crawl, đảm bảo tính tái lập và đồng bộ giữa các lần chạy | `scripts/generate_official_snapshots.py` | Done |
| Cải thiện giao diện (UI) | Viết lại giao diện Streamlit: bố cục rõ ràng hơn, hiển thị nguồn trích dẫn, trạng thái pipeline, và khu vực so sánh kết quả retrieval trực quan hơn | `app.py` | Done |
| Hỗ trợ kiểm thử | Kiểm tra dữ liệu sau crawl khớp với golden dataset; chạy acceptance tests cho phần UI và dữ liệu | `tests/test_acceptance.py` | Partial (UI test chưa cover hết retrieval) |

> Chỉ kê khai công việc có thể đối chiếu bằng file, commit, pull request, test hoặc kết quả evaluation.

---

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Chuẩn hóa dữ liệu crawl về Markdown có cấu trúc (heading, bảng, metadata nguồn) thay vì giữ nguyên PDF gốc.
   - **Lý do/evidence:** Markdown dễ chunk theo section, giữ được metadata `source`, `title`, `doc_type`; pipeline Task 4 ingest ổn định và truy vết được nguồn.
   - **Trade-off:** Tốn công chuẩn hóa thủ công ban đầu nhưng giảm lỗi chunking và tăng chất lượng retrieval về sau.

2. **Quyết định:** Viết lại UI theo hướng hiển thị minh bạch nguồn trích dẫn và trạng thái pipeline thay vì chỉ hiện câu trả lời.
   - **Lý do/evidence:** Người dùng cuối cần biết câu trả lời đến từ tài liệu nào; UI mới giúp debug retrieval nhanh hơn khi demo và kiểm thử.
   - **Trade-off:** UI phức tạp hơn, cần thêm không gian hiển thị nhưng đổi lại trải nghiệm và khả năng kiểm chứng tốt hơn.

---

## Kiểm thử và kết quả

- **Test hoặc query tôi đã dùng:** Kiểm tra thủ công dữ liệu sau crawl, đối chiếu với `golden_dataset.json`, chạy `pytest tests/test_acceptance.py -q` và chạy `streamlit run app.py` để kiểm tra UI.
- **Kết quả trước/sau nếu có:** Dữ liệu tuyển sinh HUTECH 2026 được chuẩn hóa đầy đủ và ingest thành công vào pipeline; UI mới hiển thị được nguồn trích dẫn và trạng thái pipeline rõ ràng hơn.
- **Lỗi đã phát hiện và cách xử lý:** Một số file PDF gốc có bảng và ký tự đặc biệt gây lỗi khi chuyển Markdown; đã xử lý bằng cách chuẩn hóa thủ công và kiểm tra lại từng file trước khi commit.

---

## Điều còn hạn chế

- **Một hạn chế cụ thể của phần tôi làm:** Dữ liệu crawl hiện tập trung vào tài liệu tuyển sinh HUTECH 2026, chưa mở rộng sang các nguồn khác; UI mới chưa có kiểm thử tự động đầy đủ.
- **Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện:** Viết script crawl có kiểm thử tự động và bổ sung test UI (Streamlit AppTest) để đảm bảo giao diện không bị regression.

---

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- **Ngày:** 25/09/2025
- **Tên thành viên:** Đoàn Phương Linh