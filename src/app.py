"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer - Lương Bảo Long)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.

🎯 CHỦ ĐỀ 8: Trợ Lý Duyệt Chi Phí Doanh Nghiệp (Enterprise Expense Approval Assistant)
"""

import json
import os
import re
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 1 (test_cases), Role 2 (tools) & Role 3 (prompts)
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")

    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider) -> str:
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    Chỉ dùng kiến thức tĩnh của LLM, KHÔNG được gọi Tool nào từ AVAILABLE_TOOLS.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: CHATBOT_BASELINE_PROMPT ({len(CHATBOT_BASELINE_PROMPT)} ký tự)")

    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")
    return response


# ==============================================================================
# 🔍 PARSER: trích xuất Thought / Action / Final Answer từ phản hồi LLM
# ==============================================================================
def parse_llm_output(text: str):
    """
    Parse phản hồi thô của LLM theo đúng REACT_SYSTEM_PROMPT protocol:
        Thought: ...
        Action: tool_name[arg1, arg2]
    hoặc:
        Thought: ...
        Final Answer: ...
    Trả về tuple (thought, action, final_answer) trong đó action = (tool_name, [args]) hoặc None.
    """
    thought_match = re.search(
        r"Thought:\s*(.+?)(?=\n(?:Action:|Final Answer:)|\Z)", text, re.S
    )
    action_match = re.search(r"Action:\s*([\w_]+)\s*\[(.*?)\]", text, re.S)
    final_match = re.search(r"Final Answer:\s*(.+)", text, re.S)

    thought = thought_match.group(1).strip() if thought_match else None
    final_answer = final_match.group(1).strip() if final_match else None

    action = None
    if action_match:
        tool_name = action_match.group(1).strip()
        raw_args = action_match.group(2).strip()
        args = [a.strip().strip("'\"") for a in raw_args.split(",")] if raw_args else []
        action = (tool_name, args)

    return thought, action, final_answer


# ==============================================================================
# 🛠️ EXECUTOR: gọi Tool thật từ AVAILABLE_TOOLS (Application chèn Observation thật,
# KHÔNG để LLM tự bịa Observation)
# ==============================================================================
def execute_tool(tool_name: str, args: list) -> str:
    if tool_name not in AVAILABLE_TOOLS:
        valid_tools = ", ".join(sorted(set(AVAILABLE_TOOLS.keys())))
        return f"❌ LỖI: Tool '{tool_name}' không tồn tại. Các tool hợp lệ gồm: [{valid_tools}]"
    try:
        return AVAILABLE_TOOLS[tool_name](*args)
    except TypeError as e:
        return f"❌ LỖI THAM SỐ: Gọi '{tool_name}{args}' sai cú pháp tham số. Chi tiết: {e}"
    except Exception as e:
        return f"❌ LỖI THỰC THI TOOL '{tool_name}': {e}"


def _safe_fallback(reason: str) -> str:
    """Phản hồi lịch sự khi Guardrail được kích hoạt (thay vì crash hoặc lặp vô hạn)."""
    fallback = (
        f"Xin lỗi, hồ sơ này cần được xử lý thủ công do {reason}. "
        "Đã chuyển yêu cầu cho bộ phận Tài chính kiểm tra trực tiếp."
    )
    print(f"🏁 Final Answer (Safe Fallback): {fallback}")
    return fallback


def run_react_agent(user_query: str, provider) -> str:
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails,
    gọi Tool thật từ tools.py và dừng khi có Final Answer hoặc chạm MAX_ITERATIONS.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: REACT_SYSTEM_PROMPT ({len(REACT_SYSTEM_PROMPT)} ký tự) | MAX_ITERATIONS={MAX_ITERATIONS}")

    conversation = f"Câu hỏi người dùng: {user_query}\n"
    last_actions = []  # theo dõi (tool_name, args) đã gọi để chặn lặp (Guardrail #3)
    step = 0

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        response = provider.generate(conversation, system_prompt=REACT_SYSTEM_PROMPT)
        thought, action, final_answer = parse_llm_output(response)

        if thought:
            print(f"🧠 Thought: {thought}")

        # ✅ Trường hợp 1: LLM đã đủ bằng chứng để trả lời
        if final_answer:
            print(f"🏁 Final Answer: {final_answer}")
            return final_answer

        # ⚠️ Trường hợp 2: LLM không sinh đúng Action hợp lệ -> báo lỗi & cho thử lại
        if not action:
            print("⚠️ Không parse được Action hoặc Final Answer hợp lệ trong phản hồi LLM.")
            conversation += (
                f"\nThought: {thought or '(không rõ)'}\n"
                "Observation: LỖI ĐỊNH DẠNG - Không tìm thấy Action hoặc Final Answer đúng cú pháp. "
                "Vui lòng dùng đúng cú pháp 'Action: ten_tool[tham_so]' hoặc 'Final Answer: ...'.\n"
            )
            continue

        # 🛠️ Trường hợp 3: LLM gọi Action -> thực thi Tool thật
        tool_name, args = action
        print(f"🛠️ Action: {tool_name}{args}")

        action_key = (tool_name, tuple(args))
        if last_actions.count(action_key) >= 2:
            print("🛡️ GUARDRAIL: Phát hiện lặp lại cùng Action + tham số quá 2 lần. Ngắt an toàn.")
            return _safe_fallback("hệ thống phát hiện thao tác lặp lại bất thường")
        last_actions.append(action_key)

        observation = execute_tool(tool_name, args)
        print(f"👁️ Observation: {observation}")

        conversation += (
            f"\nThought: {thought}\nAction: {tool_name}{args}\nObservation: {observation}\n"
        )

    # 🛡️ Trường hợp 4: Chạm giới hạn MAX_ITERATIONS mà chưa có Final Answer
    print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")
    return _safe_fallback(f"vượt quá số bước xử lý tự động cho phép ({MAX_ITERATIONS} bước)")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("🎯 CHỦ ĐỀ 8: TRỢ LÝ DUYỆT CHI PHÍ DOANH NGHIỆP")
    print("==================================================")

    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")

    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")

    # Test case #3 (id=3): Multi-step - Kiểm tra trạng thái hóa đơn
    tc_multi_step = next(tc for tc in tests if tc["id"] == 3)
    sample_query = tc_multi_step["question"]

    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)

    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)

    # Test case #5 (id=5): Edge Case - kiểm tra Guardrail có chặn duyệt chi sai quy định không
    print("\n--- DEMO 3: KIỂM TRA GUARDRAIL VỚI CÂU BẪY (EDGE CASE) ---")
    tc_edge_case = next(tc for tc in tests if tc["id"] == 5)
    run_react_agent(tc_edge_case["question"], provider)