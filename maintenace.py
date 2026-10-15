/****************/
Mã sinh viên: 202419007
Họ tên: Phạm Anh Tú
/****************/
Mở rộng có giải thích: hợp đồng bảo trì.

from datetime import date


class MaintenanceContract:
    """Quản lý hợp đồng bảo trì dịch vụ gắn với thiết bị."""

    def __init__(self, contract_id, supplier, device, start_date, end_date, annual_fee):
        if not contract_id:
            raise ValueError("Mã hợp đồng không được rỗng.")
        if not supplier:
            raise ValueError("Đơn vị cung cấp không được rỗng.")
        if device is None:
            raise ValueError("Thiết bị hợp đồng không hợp lệ.")
        if end_date < start_date:
            raise ValueError("Ngày kết thúc hợp đồng không được trước ngày bắt đầu.")
        if annual_fee <= 0:
            raise ValueError("Phí hợp đồng phải lớn hơn 0.")

        self.contract_id = contract_id
        self.supplier = supplier
        self.device = device
        self.start_date = start_date
        self.end_date = end_date
        self.annual_fee = annual_fee

    def is_active(self, on_date):
        """Kiểm tra xem hợp đồng có đang còn hiệu lực vào ngày truyền vào không."""
        return self.start_date <= on_date <= self.end_date