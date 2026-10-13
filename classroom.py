/****************/
Mã sinh viên: 202419007	
Họ tên: Phạm Anh Tú
/****************/

from datetime import date


class ClassRoom:
    """Quản lý phòng học và danh sách thiết bị trong phòng."""

    def __init__(self, room_id, room_name, capacity):
        if not room_id:
            raise ValueError("Mã phòng không được trống.")
        if not room_name:
            raise ValueError("Tên phòng không được trống.")
        if capacity <= 0:
            raise ValueError("Sức chứa phải lớn hơn 0.")

        self.room_id = room_id
        self.room_name = room_name
        self.capacity = capacity
        self.devices = []  # Dùng danh sách (list) thông thường để chứa thiết bị

    def add_device(self, device):
        """Thêm thiết bị vào phòng học."""
        if device is None:
            raise ValueError("Thiết bị không hợp lệ.")

        # Kiểm tra xem thiết bị đã có trong phòng chưa
        for d in self.devices:
            if d.device_id == device.device_id:
                raise ValueError("Thiết bị này đã có trong phòng rồi.")

        self.devices.append(device)

    def remove_device(self, device_id):
        """Xóa thiết bị khỏi phòng dựa vào mã thiết bị."""
        for d in self.devices:
            if d.device_id == device_id:
                self.devices.remove(d)
                return True
        return False

    def find_device(self, device_id):
        """Tìm và trả về thiết bị theo mã, nếu không thấy trả về None."""
        for d in self.devices:
            if d.device_id == device_id:
                return d
        return None

    def calculate_annual_maintenance_cost(self):
        """Tính tổng chi phí bảo trì hằng năm của tất cả thiết bị trong phòng."""
        total_cost = 0
        for device in self.devices:
            total_cost += device.calculate_annual_maintenance_cost()
        return total_cost

    def get_devices_requiring_maintenance(self, today=None):
        """Lấy danh sách các thiết bị cần bảo trì."""
        if today is None:
            today = date.today()

        result = []
        for device in self.devices:
            # Điều kiện cần bảo trì: đang bảo trì HOẶC dùng đã quá 5 năm
            if device.status == "UNDER_MAINTENANCE" or (today.year - device.introduced_year > 5):
                result.append(device)
        return result