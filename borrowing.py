/****************/
Mã sinh viên: 202419007
Họ tên: Phạm Anh Tú
/****************/

from datetime import datetime, timedelta

# Đơn giá phạt trễ cố định 
LATE_FEE_PER_DAY = 20000


class BorrowItem:
    """Một thiết bị nằm trong phiếu mượn."""

    def __init__(self, device, borrowed_date, borrow_days, from_period=1, to_period=1):
        # Kiểm tra cơ bản
        if device is None:
            raise ValueError("Thiết bị không được để trống.")
        
        if borrow_days < 1 or borrow_days > device.max_borrow_days:
            raise ValueError("Số ngày mượn không hợp lệ.")

        self.device = device
        self.borrowed_date = borrowed_date
        self.borrow_days = borrow_days
        
        # Tính ngày đến hạn (due_date) bằng ngày mượn cộng thêm số ngày mượn
        self.due_date = borrowed_date + timedelta(days=borrow_days)
        
        self.from_period = from_period
        self.to_period = to_period
        self.returned_date = None  # Chưa trả thì để là None

    @property
    def is_returned(self):
        """Kiểm tra xem thiết bị đã được trả chưa."""
        return self.returned_date is not None

    def return_item(self, returned_date):
        """Xử lý trả thiết bị này."""
        if self.is_returned:
            raise ValueError("Thiết bị này đã được trả trước đó rồi.")
        if returned_date < self.borrowed_date:
            raise ValueError("Ngày trả không được trước ngày mượn.")
        
        self.returned_date = returned_date

    def calculate_late_fee(self, as_of=None):
        """Tính tiền phạt trễ hạn cho thiết bị này."""
        checked_date = self.returned_date
        if checked_date is None:
            if as_of is None:
                return 0
            checked_date = as_of

        # Tính số ngày trễ (so sánh ngày)
        days_late = (checked_date.date() - self.due_date.date()).days
        if days_late > 0:
            return days_late * LATE_FEE_PER_DAY
        return 0


class BorrowingSlip:
    """Phiếu mượn thiết bị của một người."""

    def __init__(self, slip_id, borrower, teaching_room, borrowed_date):
        if not slip_id:
            raise ValueError("Mã phiếu không được trống.")
        if borrower is None:
            raise ValueError("Người mượn không được trống.")
        if not teaching_room:
            raise ValueError("Phòng học không được trống.")

        self.slip_id = slip_id
        self.borrower = borrower
        self.teaching_room = teaching_room
        self.borrowed_date = borrowed_date
        self.items = []  # Danh sách các thiết bị được mượn trong phiếu

    def add_device(self, device, borrow_days, from_period=1, to_period=1):
        """Thêm thiết bị vào phiếu mượn."""
        if device is None:
            raise ValueError("Thiết bị không hợp lệ.")

        # Kiểm tra xem thiết bị đã có trong phiếu chưa
        for item in self.items:
            if item.device.device_id == device.device_id:
                raise ValueError("Thiết bị này đã có trong phiếu mượn rồi.")

        # Kiểm tra giới hạn số lượng thiết bị của người mượn
        max_devices = self.borrower.get_maximum_devices()
        if len(self.items) >= max_devices:
            raise ValueError("Đã vượt quá số lượng thiết bị cho phép mượn.")

        # Kiểm tra thiết bị có đang sẵn sàng cho mượn không
        # (Giả sử DeviceStatus.AVAILABLE có giá trị nào đó, ví dụ chữ 'AVAILABLE')
        if device.status != "AVAILABLE":
            raise ValueError("Thiết bị hiện không sẵn sàng để mượn.")

        # Tạo mục mượn mới và thêm vào danh sách
        item = BorrowItem(device, self.borrowed_date, borrow_days, from_period, to_period)
        
        # Đánh dấu thiết bị là đã bị mượn
        device.mark_as_borrowed()
        self.items.append(item)

    def return_device(self, device_id, returned_date):
        """Trả một thiết bị theo mã thiết bị."""
        if not device_id:
            raise ValueError("Mã thiết bị không hợp lệ.")

        # Tìm thiết bị trong phiếu
        target_item = None
        for item in self.items:
            if item.device.device_id == device_id:
                target_item = item
                break

        if target_item is None:
            raise ValueError("Không tìm thấy thiết bị này trong phiếu mượn.")

        # Thực hiện trả thiết bị
        target_item.return_item(returned_date)
        target_item.device.mark_as_available()

        return target_item.calculate_late_fee()

    def calculate_total_late_fee(self, as_of=None):
        """Tính tổng tiền phạt của tất cả thiết bị trong phiếu."""
        total = 0
        for item in self.items:
            total += item.calculate_late_fee(as_of)
        return total

    def get_overdue_items(self, as_of):
        """Lấy danh sách các thiết bị đang bị quá hạn."""
        overdue_list = []
        for item in self.items:
            if not item.is_returned and as_of > item.due_date:
                overdue_list.append(item)
        return overdue_list

    def get_unreturned_items(self):
        """Lấy danh sách các thiết bị chưa được trả."""
        unreturned_list = []
        for item in self.items:
            if not item.is_returned:
                unreturned_list.append(item)
        return unreturned_list