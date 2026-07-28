# 📋 SỔ TAY PHÂN CÔNG & CHECKLIST THỰC HÀNH (ZERO-CONFLICT WORKFLOW)

> 💡 **Hướng dẫn**: Mỗi thành viên mở đúng file được phân công trong thư mục dự án và thực hiện checklist theo từng Mốc.

---

## 👥 1. BẢNG PHÂN VAI & FILE ĐẢM NHẬN

> ⚠️ **Nhóm chỉ có 3 thành viên** trong khi Lab thiết kế cho 5 Role. Để **không ai đụng chung 1 file cùng lúc** (Zero-Conflict), ta gộp Role theo nguyên tắc: mỗi người sở hữu trọn vẹn 1-2 file riêng biệt, không chia đôi 1 file cho 2 người.

| Người đảm nhận | Role gộp | File đảm nhận | Nhiệm vụ chính |
| :--- | :--- | :--- | :--- |
| **Phan Hoàng Dũng** | Role 1 (Product Architect) + Role 5 (Observability) | `config/test_cases.json`<br>`docs/trace_eval.md` | Định hướng bài toán, soạn bộ test case; lập Scoring Matrix & ghi nhật ký Trace Log so sánh Chatbot vs Agent |
| **Ngô Nguyễn Khải Hưng** | Role 2 (Tool Engineer) + Role 3 (Prompt Engineer) | `src/tools.py`<br>`src/prompts.py` | Định nghĩa & viết docstring cho các Tools; soạn Chatbot Baseline Prompt, ReAct System Prompt và phanh Guardrails (`MAX_ITERATIONS`) |
| **Lương Bảo Long** | Role 4 (Core Developer / Integrator) | `src/app.py` | **Đầu mối duy nhất kéo code (`git pull`) và Vibe Code lắp ráp** `tools.py` + `prompts.py` + `test_cases.json` thành App hoàn chỉnh (`run_baseline_chatbot()`, `run_react_agent()`) |

**Vì sao cách gộp này không xung đột:**
- Mỗi người có **file riêng, không ai trùng file** ⇒ khi `git push` không ai đè code của nhau.
- Dũng (test case + trace log) và Hưng (tools + prompts) là 2 nhánh **độc lập song song** — có thể làm cùng lúc mà không cần chờ nhau.
- Long chỉ cần `git pull` sau khi Dũng & Hưng đã push, rồi mới bắt tay lắp `app.py` — tránh việc 3 người cùng sửa 1 file lõi.
- Khi cần dữ liệu để viết trace log, Dũng **đợi Long chạy xong `app.py`** rồi mới điền `docs/trace_eval.md`, thay vì code song song trên cùng file `app.py`.

*Ghi chú: Ở Mốc 4 (Hybrid Flowchart), file mới `docs/hybrid_flowchart.mermaid` do **Dũng** đảm nhận tiếp (vì đã quen `docs/`), không tạo file mới chồng lấn với Long hay Hưng.*

> 🌟 **VAI TRÒ NÒNG NỐT CỦA ROLE 4 (ĐẦU MỐI LẮP RÁP APP HOÀN CHỈNH)**:
>
> - **Role 4** đóng vai trò là **Tổ trưởng Lắp ráp**: Sau khi các bạn Role 1, 2, 3 đẩy file lên Git, **Role 4 sẽ gõ `git pull`** để gom toàn bộ dữ liệu về máy.
> - **Role 4** sau đó dùng AI (Vibe Code) để kết nối `tools.py`, `prompts.py`, `test_cases.json` vào file `src/app.py`, biến các mảnh ghép thành **một Ứng dụng AI Agent hoàn chỉnh** cho cả nhóm chạy nghiệm thu.

---

## ⏱️ 2. CHECKLIST THỰC HÀNH THEO 4 MỐC

### 📍 MỐC 1: Định hình & Đánh giá độ phù hợp (Agentic Fit) (20 phút)

*Mục tiêu: Chứng minh bài toán này CẦN dùng Agent chứ không chỉ Chatbot.*

- [ ] **Dũng (Role 1) & Cả nhóm**: **Tự do lựa chọn 1 chủ đề bài toán thực tế** mà nhóm hào hứng nhất (Xem 10 đề tài gợi ý tại: [DANH_SACH_DE_TAI.md](file:///c:/Users/Admin/Documents/VinUni/LabCoachVin/LabKeyCoach/Day-3-Lab-Chatbot-vs-react-agent-E402/docs/DANH_SACH_DE_TAI.md)).
- [ ] **Dũng (Role 5)**: Điền bảng **Scoring Matrix** (chấm 1–5 điểm cho 4 tiêu chí) vào `docs/trace_eval.md`.
- [ ] **Hưng (Role 2)**: Liệt kê tên các công cụ sẽ tạo trong `src/tools.py` phù hợp với chủ đề nhóm đã chọn.
- [ ] **Hưng (Role 3)**: Xác định các trường hợp tool có thể bị lỗi (Failure Modes) — ghi chú tạm ngay trong `src/tools.py` để dùng ở Mốc 3.
- [ ] **Long (Role 4)**: Mở Terminal gõ `python src/app.py` kiểm tra xem môi trường sẵn sàng chưa.
- [ ] 🤝 **Cả nhóm**: Gật đầu thống nhất bài toán trước khi sang Mốc 2.
- [ ] 🔄 **Đồng bộ Git Mốc 1**: Cả nhóm lưu file, đẩy code lên Git: `git add .` ➔ `git commit -m "Moc 1: Scoring Matrix & Dinh hinh"` ➔ `git push`.

---

### 📍 MỐC 2: Baseline Chatbot & Khai báo Tool Specs (30 phút)

*Mục tiêu: Thấy rõ hạn chế của Chatbot gốc và chuẩn hóa công cụ cho Agent.*

- [ ] **Dũng (Role 1)**: Viết bộ **Test Cases** vào file `config/test_cases.json` (câu đơn giản, câu multi-step, câu bẫy).
- [ ] **Hưng (Role 2)**: Dùng AI bổ sung Docstring / Mô tả chuẩn cho các hàm trong `src/tools.py`.
- [ ] **Hưng (Role 3)**: Soạn `CHATBOT_BASELINE_PROMPT` trong file `src/prompts.py`.
- [ ] **Long (Role 4 — Đầu mối Lắp ráp)**: Gõ `git pull` để kéo file của Dũng & Hưng về máy ➔ Vibe Code nối `run_baseline_chatbot()` trong `src/app.py` và bấm chạy thử.
- [ ] **Dũng (Role 5)**: Ghi lại phản hồi của Chatbot gốc vào `docs/trace_eval.md` (quan sát xem Chatbot có bị ảo giác/không biết thông tin thực tế không) — thực hiện **sau khi Long chạy xong `app.py`**.
- [ ] 🔄 **Đồng bộ Git Mốc 2**: Cả nhóm lưu file, đẩy code lên Git: `git add .` ➔ `git commit -m "Moc 2: Chatbot Baseline & Tool Specs"` ➔ `git push`.

---

### 📍 MỐC 3: ReAct Loop & Safeguards (60 phút)

*Mục tiêu: Dựng ReAct Agent suy luận Thought -> Action và cài phanh an toàn.*

- [ ] **Hưng (Role 3)**: Soạn `REACT_SYSTEM_PROMPT` (ép AI sinh Thought -> Action) và đặt `MAX_ITERATIONS (giới hạn số lần lặp)` trong `src/prompts.py`.
- [ ] **Hưng (Role 2)**: Đảm bảo các hàm trong `src/tools.py` khi gặp lỗi sẽ trả về chuỗi thông báo lỗi chứ không crash code.
- [ ] **Long (Role 4 — Đầu mối Lắp ráp & Vibe App)**: Gõ `git pull` kéo toàn bộ code mới nhất ➔ Vibe Code lắp vòng lặp ReAct Agent Loop hoàn chỉnh trong `src/app.py` và chạy thử nghiệm.
- [ ] **Dũng (Role 5)**: Trích xuất chuỗi `Thought -> Action -> Observation` dán vào `docs/trace_eval.md`.
- [ ] **Dũng (Role 1)**: Kiểm tra xem Agent có vượt qua được câu bẫy (Edge Case) bằng phanh Guardrail hay không.
- [ ] 🔄 **Đồng bộ Git Mốc 3**: Cả nhóm lưu file, đẩy code lên Git: `git add .` ➔ `git commit -m "Moc 3: ReAct Agent Loop & Safeguards"` ➔ `git push`.

---

### 📍 MỐC 4: Tương tác liên nhóm & Hybrid Flowchart (40 phút)

*Mục tiêu: Thử thách khả năng chịu lỗi trước đòn tấn công từ nhóm khác & Chấm chéo linh hoạt.*

> 💡 **HÌNH THỨC TƯƠNG TÁC (Tùy Giảng viên chỉ định)**:
>
> * 🎲 **Hình thức 1 (Gọi ngẫu nhiên)**: Giảng viên gọi ngẫu nhiên một thành viên đại diện trong bất kỳ nhóm nào lên trình chiếu App, phản biện và trả lời câu hỏi bẫy từ các nhóm khác.
> * 🔄 **Hình thức 2 (Chấm chéo nhóm)**: Giảng viên chỉ định 1 bạn đại diện (gợi ý: **Dũng**, vì đã nắm rõ bộ test case) đi sang nhóm khác để "tấn công" (dùng câu bẫy thử nghiệm Agent nhóm bạn) và chấm điểm chéo. **Long** đứng trình chiếu App tại chỗ vì là người nắm rõ `app.py` nhất.

- [ ] ⚔️ **Đội Tấn Công (Đại diện/Học viên được gọi)**: Mang các câu test case của nhóm mình sang "xả" vào Agent của Nhóm bạn để kiểm thử khả năng chịu lỗi.
- [ ] 🛡️ **Đội Phòng Thủ**: Quan sát Agent nhóm mình phản ứng trước câu hỏi của nhóm bạn. Kiểm tra xem Guardrail bảo vệ an toàn không.
- [ ] 📊 **Dũng (Role 5)**: Vẽ sơ đồ **Hybrid Flowchart** vào file `docs/hybrid_flowchart.mermaid` thể hiện phân luồng:
  - Câu hỏi đơn giản ➔ Đi đường Chatbot path.
  - Câu hỏi phức tạp ➔ Đi đường ReAct Agent path.
- [ ] 🔄 **Đồng bộ Git Mốc 4 (Hoàn thành)**: Cả nhóm lưu file, đẩy bản hoàn chỉnh lên Git: `git add .` ➔ `git commit -m "Moc 4: Cross Audit & Hybrid Flowchart Hoan thanh"` ➔ `git push`.

---

Vì mỗi thành viên giữ đúng 1 file trong các thư mục riêng (`config/`, `src/`, `docs/`), bạn chỉ cần nhớ quy trình :

**Trước khi gõ code**: Kéo code mới của nhóm về:

```bash
   git pull
```

**Đẩy code lên cho nhóm**:

```bash
   git add .
   git commit -m "Role X: cap nhat noi dung"
   git push
```

*(Nếu push bị chặn do bạn khác push trước: Gõ `git pull` rồi `git push` lại là xong!)*