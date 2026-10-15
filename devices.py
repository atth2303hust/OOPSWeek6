/****************/
Mã sinh viên: 202419007
Họ tên: Phạm Anh Tú
/****************/

from abc import ABC, abstractmethod
from datetime import date


class Device(ABC):
    """Lớp trừu tượng quản lý thông tin chung của thiết bị."""

    def __init__(self, device_id, name, introduced_year, purchase_price, status="Available"):
        if not device_id:
            raise ValueError("Mã thiết bị không được rỗng.")
        if not name:
            raise ValueError("Tên thiết bị không được rỗng.")
        if introduced_year < 1 or introduced_year > date.today().year:
            raise ValueError("Năm sản xuất/sử dụng không hợp lệ.")
        if purchase_price <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")

        self.device_id = device_id
        self.name = name
        self.introduced_year = introduced_year
        self.purchase_price = purchase_price
        self.status = status  # Trạng thái: "Available", "Borrowed", "UnderMaintenance", "Retired"

    def mark_as_borrowed(self):
        """Đánh dấu thiết bị là đang được mượn."""
        if self.status != "Available":
            raise ValueError("Thiết bị không sẵn sàng để mượn.")
        self.status = "Borrowed"

    def mark_as_available(self):
        """Đánh dấu thiết bị đã được trả và trở lại sẵn sàng."""
        if self.status != "Borrowed":
            raise ValueError("Thiết bị không ở trạng thái đang mượn.")
        self.status = "Available"

    def send_to_maintenance(self):
        """Gửi thiết bị đi bảo trì."""
        if self.status != "Available":
            raise ValueError("Chỉ có thiết bị sẵn sàng mới được mang đi bảo trì.")
        self.status = "UnderMaintenance"

    def finish_maintenance(self):
        """Hoàn tất bảo trì."""
        if self.status != "UnderMaintenance":
            raise ValueError("Thiết bị không ở trạng thái bảo trì.")
        self.status = "Available"

    @abstractmethod
    def calculate_annual_maintenance_cost(self):
        """Tính chi phí bảo trì hằng năm (phải được định nghĩa ở lớp con)."""
        pass


class TeachingDevice(Device, ABC):
    """Thiết bị giảng dạy (có giới hạn ngày và số tiết mượn riêng)."""
    max_borrow_days = 0
    max_borrow_periods = 0


class ProjectorRemote(TeachingDevice):
    """Điều khiển máy chiếu: mượn tối đa 5 ngày, 6 tiết."""
    max_borrow_days = 5
    max_borrow_periods = 6

    def calculate_annual_maintenance_cost(self):
        # Chi phí bảo trì bằng 5% giá mua
        return self.purchase_price * 0.05


class AirConditionerRemote(TeachingDevice):
    """Điều khiển điều hòa: mượn tối đa 2 ngày, 8 tiết."""
    max_borrow_days = 2
    max_borrow_periods = 8

    def calculate_annual_maintenance_cost(self):
        # Chi phí bảo trì bằng 4% giá mua
        return self.purchase_price * 0.04


class WirelessMicrophone(TeachingDevice):
    """Micro không dây: mượn tối đa 1 ngày, 4 tiết."""
    max_borrow_days = 1
    max_borrow_periods = 4

    def calculate_annual_maintenance_cost(self):
        # Chi phí bảo trì bằng 10% giá mua
        return self.purchase_price * 0.10