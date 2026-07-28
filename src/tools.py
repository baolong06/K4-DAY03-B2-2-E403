"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi cho Chủ đề 8: Trợ Lý Duyệt Chi Phí Doanh Nghiệp.
"""

def get_expense_policy(category: str) -> str:
    """
    Tra cứu quy định và hạn mức chi tiêu tối đa cho 1 lần chi theo hạng mục.
    
    Args:
        category (str): Tên hạng mục (Ví dụ: 'Tiếp khách', 'Công tác phí', 'Mua sắm thiết bị', 'Đào tạo')
        
    Returns:
        str: Thông tin hạn mức và điều kiện phê duyệt
    """
    cat_clean = category.strip().lower()
    if "tiếp khách" in cat_clean or "tiep khach" in cat_clean:
        return "Hạng mục 'Tiếp khách': hạn mức tối đa 3.000.000 VNĐ/lần, vượt mức phải có phê duyệt của Trưởng phòng."
    elif "công tác" in cat_clean or "cong tac" in cat_clean:
        return "Hạng mục 'Công tác phí': hạn mức di chuyển/lưu trú tối đa 5.000.000 VNĐ/chuyến. Yêu cầu hóa đơn tài chính hợp lệ."
    elif "thiết bị" in cat_clean or "thiet bi" in cat_clean or "mua sắm" in cat_clean:
        return "Hạng mục 'Mua sắm thiết bị': hạn mức tối đa 10.000.000 VNĐ/thiết bị. Cần ít nhất 2 báo giá cạnh tranh."
    elif "đào tạo" in cat_clean or "dao tao" in cat_clean:
        return "Hạng mục 'Đào tạo': hạn mức tối đa 7.000.000 VNĐ/khóa/nhân viên. Yêu cầu cam kết phục vụ 6 tháng."
    else:
        return f"Hạng mục '{category}': hạn mức tiêu chuẩn tối đa 2.000.000 VNĐ/lần chi. Cần duyệt bởi quản lý trực tiếp."


def check_budget_remaining(department: str) -> str:
    """
    Tra cứu số dư ngân sách khả dụng còn lại trong tháng của một phòng ban.
    
    Args:
        department (str): Tên phòng ban (Ví dụ: 'Kinh Doanh', 'Kỹ Thuật', 'Nhân Sự', 'Marketing')
        
    Returns:
        str: Thông tin số dư ngân sách còn lại
    """
    dept_clean = department.strip().lower()
    if "kinh doanh" in dept_clean or "sales" in dept_clean:
        return "Ngân sách phòng Kinh Doanh còn lại tháng này: 12.000.000 VNĐ (đủ để chi thêm)."
    elif "kỹ thuật" in dept_clean or "it" in dept_clean or "tech" in dept_clean:
        return "Ngân sách phòng Kỹ Thuật còn lại tháng này: 60.000.000 VNĐ (đủ để chi thêm)."
    elif "nhân sự" in dept_clean or "hr" in dept_clean:
        return "Ngân sách phòng Nhân Sự còn lại tháng này: 1.500.000 VNĐ (sắp hết ngân sách)."
    elif "marketing" in dept_clean:
        return "Ngân sách phòng Marketing còn lại tháng này: 80.000.000 VNĐ (đủ để chi thêm)."
    else:
        return f"Ngân sách phòng {department} còn lại tháng này: 10.000.000 VNĐ (đủ để chi thêm)."


def get_employee_expense_history(employee_name: str) -> str:
    """
    Tra cứu lịch sử đề xuất chi tiêu và hạn mức cá nhân của nhân viên trong tháng.
    
    Args:
        employee_name (str): Tên nhân viên (Ví dụ: 'Nguyễn Văn A', 'Trần Thị B')
        
    Returns:
        str: Tổng số tiền đã chi và mức độ tuân thủ
    """
    emp_clean = employee_name.strip().lower()
    if "nguyễn văn a" in emp_clean or "nguyen van a" in emp_clean or "văn a" in emp_clean:
        return "Nhân viên Nguyễn Văn A | Số lần đề xuất tháng này: 2 | Tổng số tiền đã chi: 4,500,000 VNĐ | Lịch sử tuân thủ: Tốt, chưa có vi phạm."
    elif "trần thị b" in emp_clean or "tran thi b" in emp_clean:
        return "Nhân viên Trần Thị B | Số lần đề xuất tháng này: 5 | Tổng số tiền đã chi: 18,200,000 VNĐ | Lịch sử tuân thủ: Bình thường."
    else:
        return f"Nhân viên {employee_name} | Số lần đề xuất tháng này: 1 | Tổng số tiền đã chi: 1,200,000 VNĐ | Lịch sử tuân thủ: Tốt."


def check_invoice(invoice_id: str) -> str:
    """
    Kiểm tra tính hợp pháp, hợp lệ của hóa đơn/chứng từ đính kèm.
    
    Args:
        invoice_id (str): Mã hóa đơn (Ví dụ: 'HD-10294', 'HD-8821')
        
    Returns:
        str: Trạng thái hợp lệ của hóa đơn và thông tin chi tiết
    """
    inv_clean = invoice_id.strip().upper()
    if "HD-10294" in inv_clean or "10294" in inv_clean:
        return "Hóa đơn HD-10294 | Nhân viên: Nguyễn Văn A | Số tiền: 3,500,000 VNĐ | Nội dung: Tiếp khách | Trạng thái: Hợp lệ."
    elif "HD-8821" in inv_clean or "8821" in inv_clean:
        return "Hóa đơn HD-8821 | Nhân viên: Trần Thị B | Số tiền: 15,000,000 VNĐ | Nội dung: Mua sắm thiết bị | Trạng thái: Hợp lệ."
    else:
        return f"Hóa đơn {invoice_id} | Trạng thái: HỢP LỆ (Hóa đơn điện tử hợp pháp)."


def submit_expense_approval(claim_id: str, status: str, reason: str = "") -> str:
    """
    Cập nhật kết quả thẩm định hồ sơ chi phí lên hệ thống tài chính.
    
    Args:
        claim_id (str): Mã đề xuất chi phí (Ví dụ: 'DX-001', 'DX-3500')
        status (str): Trạng thái ('Approved', 'Rejected', 'Escalated', 'Requires_Info')
        reason (str): Lý do chi tiết
        
    Returns:
        str: Thông báo kết quả cập nhật hệ thống
    """
    return f"Đã cập nhật hệ thống tài chính: Đề xuất {claim_id} | Trạng thái: {status.upper()} | Lý do: {reason if reason else 'Đã thẩm định theo chính sách.'}"


# Tên bí danh phụ hỗ trợ tương thích ngược
check_invoice_status = check_invoice
check_department_budget = check_budget_remaining
approve_expense_request = submit_expense_approval


# Danh sách tất cả các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "get_expense_policy": get_expense_policy,
    "check_budget_remaining": check_budget_remaining,
    "check_department_budget": check_budget_remaining,
    "get_employee_expense_history": get_employee_expense_history,
    "check_invoice": check_invoice,
    "check_invoice_status": check_invoice,
    "submit_expense_approval": submit_expense_approval,
    "approve_expense_request": submit_expense_approval,
}