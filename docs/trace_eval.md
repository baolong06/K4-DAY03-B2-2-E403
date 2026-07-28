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

**Câu hỏi**: *"Kiểm tra trạng thái hóa đơn chi phí taxi mã HD-10294 của nhân viên Nguyễn Văn A."*

### 🤖 Chatbot Baseline:
* **Phản hồi**: *"Rất tiếc, tôi là phiên bản Chatbot Baseline không có khả năng truy xuất số liệu thực tế hay thẩm định hồ sơ chi tiết để kiểm tra trạng thái của một hóa đơn cụ thể.

Vui lòng chuyển sang ReAct Agent (Hệ thống duyệt chi tự động có tích hợp Tool) để xử lý yêu cầu này và kiểm tra trạng thái hóa đơn HD-10294 của nhân viên Nguyễn Văn A."*
* **Nhận xét**: Chatbot Baseline hoạt động đúng theo cấu hình prompt — tự biết hạn chế không có công cụ tra cứu cơ sở dữ liệu thực tế nên từ chối trả lời thay vì tự bịa ra trạng thái hóa đơn. Tuy nhiên, nó không giúp ích gì cho người dùng trong việc giải quyết nghiệp vụ thẩm định.

### 🧠 ReAct Agent:
* **Thought 1**: Người dùng yêu cầu kiểm tra trạng thái của một hóa đơn cụ thể. Công cụ `check_invoice_status` được thiết kế để thực hiện việc này. Tôi sẽ sử dụng mã hóa đơn 'HD-10294' làm tham số.
* **Action 1**: `check_invoice_status['HD-10294']`
* **Observation 1**: `Hóa đơn HD-10294 | Nhân viên: Nguyễn Văn A | Số tiền: 3,500,000 VNĐ | Nội dung: Tiếp khách | Trạng thái:: Hợp lệ.`
* **Thought 2**: Người dùng đã yêu cầu kiểm tra trạng thái của một hóa đơn cụ thể. Tôi đã sử dụng công cụ `check_invoice_status` và nhận được thông tin chi tiết về hóa đơn đó. Kết quả cho thấy hóa đơn HD-10294 của nhân viên Nguyễn Văn A, số tiền 3,500,000 VNĐ, nội dung "Tiếp khách" và trạng thái là "Hợp lệ". Đây là tất cả thông tin mà người dùng đã hỏi.
Tôi đã thu thập đủ bằng chứng từ các công cụ (chính sách, ngân sách, hóa đơn). Tôi sẵn sàng đưa ra kết luận.
* **Final Answer**: *"(1) Thông tin hóa đơn: HD-10294, số tiền 3,500,000 VNĐ, nội dung "Tiếp khách", nhân viên Nguyễn Văn A. 
(2) Tình trạng ngân sách phòng ban còn lại: Không có thông tin phòng ban được cung cấp, nên không thể kiểm tra ngân sách.
(3) Tính hợp lệ chứng từ: Hóa đơn HD-10294 được xác nhận là Hợp lệ.
(4) Quyết định duyệt: Để đưa ra quyết định duyệt cuối cùng, cần có thêm thông tin về mã đề xuất chi phí, phòng ban và chính sách hạn mức cho hạng mục "Tiếp khách". With thông tin hiện tại, tôi chỉ có thể xác nhận trạng thái hợp lệ của hóa đơn."*
* **Nhận xét**: ReAct Agent đã gọi đúng công cụ `check_invoice_status` để lấy dữ liệu hóa đơn thời gian thực. Ngoài ra, Agent thể hiện tư duy chặt chẽ khi xác nhận tính hợp lệ của chứng từ nhưng chỉ ra rõ những thông tin còn thiếu (phòng ban, mã đề xuất, chính sách hạn mức) trước khi đưa ra quyết định duyệt chính thức, giúp tránh rủi ro duyệt thiếu căn cứ.