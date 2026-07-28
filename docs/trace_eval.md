# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer*

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

**Đề tài**: Trợ Lý Duyệt Chi Phí Doanh Nghiệp (Enterprise Expense Approval Assistant)

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `4/5` | Cần suy luận qua nhiều bước: đọc thông tin đề nghị chi (số tiền, hạng mục, phòng ban) → đối chiếu với chính sách công ty → kiểm tra hạn mức ngân sách còn lại → kết luận duyệt/từ chối/chuyển cấp trên. |
| 🛠️ **Tool Interaction** | `5/5` | Bắt buộc tra cứu dữ liệu thực tế qua nhiều nguồn: API/CSDL chính sách chi tiêu (`get_expense_policy`), API ngân sách phòng ban (`check_budget_remaining`), lịch sử chi tiêu nhân viên (`get_employee_expense_history`) — không thể trả lời chính xác nếu chỉ dựa vào kiến thức tĩnh của LLM. |
| 🔀 **Dynamic Decision** | `5/5` | Hành động bước sau phụ thuộc hoàn toàn vào kết quả bước trước: nếu vượt hạn mức tự động duyệt → phải gọi thêm tool tìm người quản lý cấp trên để escalate; nếu hóa đơn thiếu hợp lệ → phải yêu cầu bổ sung thay vì duyệt ngay. |
| ⏳ **Long Horizon** | `4/5` | Quy trình có thể kéo dài 3-4 bước xử lý nối tiếp (kiểm tra hóa đơn → đối chiếu chính sách → kiểm tra ngân sách → xác định cấp duyệt phù hợp), phức tạp hơn một tác vụ tra cứu đơn lẻ. |
| **TỔNG ĐIỂM FIT** | **18/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT — chatbot thuần không thể tra cứu chính sách/ngân sách thực tế và không thể tự quyết định leo thang phê duyệt.** |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #3)

**Câu hỏi**: *"Nhân viên Nguyễn Văn A đề nghị duyệt chi 3.500.000 VNĐ cho hạng mục 'Tiếp khách' thuộc phòng Kinh Doanh. Đề nghị này có được duyệt không?"*

### 🤖 Chatbot Baseline:
* **Phản hồi**: *"Khoản chi 3.500.000 VNĐ cho tiếp khách nghe có vẻ hợp lý và thường nằm trong mức cho phép của nhiều công ty, nên có thể duyệt."*
* **Nhận xét**: Câu trả lời nghe thuyết phục nhưng hoàn toàn là suy đoán — chatbot không hề biết hạn mức thực tế của phòng Kinh Doanh, không biết ngân sách còn lại bao nhiêu, và không kiểm tra chính sách công ty. Nếu làm theo có thể duyệt sai, gây rủi ro tài chính thực tế.

### 🧠 ReAct Agent:
* **Thought 1**: Cần tra cứu chính sách chi tiêu cho hạng mục "Tiếp khách" để biết hạn mức tối đa.
* **Action 1**: `get_expense_policy['Tiếp khách']`
* **Observation 1**: `Hạng mục "Tiếp khách": hạn mức tối đa 3.000.000 VNĐ/lần, vượt mức phải có phê duyệt của Trưởng phòng.`
* **Thought 2**: Khoản đề nghị (3.500.000 VNĐ) vượt hạn mức cho phép, cần kiểm tra ngân sách còn lại của phòng Kinh Doanh trước khi quyết định hướng xử lý.
* **Action 2**: `check_budget_remaining['Kinh Doanh']`
* **Observation 2**: `Ngân sách phòng Kinh Doanh còn lại tháng này: 12.000.000 VNĐ (đủ để chi thêm).`
* **Thought 3**: Ngân sách còn đủ, nhưng vì khoản chi vượt hạn mức/lần theo chính sách nên không thể tự động duyệt — phải chuyển lên Trưởng phòng phê duyệt.
* **Final Answer**: *"Khoản chi 3.500.000 VNĐ vượt hạn mức tiếp khách cho phép (3.000.000 VNĐ/lần) theo chính sách công ty. Ngân sách phòng Kinh Doanh vẫn còn đủ, nhưng đề nghị này cần được Trưởng phòng phê duyệt trước khi giải ngân. Đã chuyển yêu cầu lên bước phê duyệt cấp cao hơn."*
* **Nhận xét**: Agent đưa ra quyết định có căn cứ thực tế (policy + ngân sách), phát hiện đúng trường hợp cần escalate thay vì tự ý duyệt/từ chối — điều mà Chatbot Baseline không làm được vì không có dữ liệu thật.