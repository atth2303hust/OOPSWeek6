/****************/
Mã sinh viên: 20419007
Họ tên: Phạm Anh Tú
/****************/
Các ngoại lệ nghiệp vụ mượn/trả thiết bị.
"""


class BorrowingException(Exception):
    """Lớp cha cho mọi lỗi phát sinh trong nghiệp vụ mượn/trả."""
    pass


class DeviceUnavailableException(BorrowingException):
    """Thiết bị không ở trạng thái cho mượn."""
    def __init__(self, message):
        super().__init__(message)


class BorrowLimitExceededException(BorrowingException):
    """Người mượn đã đạt số thiết bị tối đa trên một phiếu."""
    def __init__(self, message):
        super().__init__(message)


class InvalidBorrowPeriodException(BorrowingException):
    """Thời hạn mượn hoặc khoảng tiết mượn không hợp lệ."""
    def __init__(self, message):
        super().__init__(message)


class DuplicateDeviceException(BorrowingException):
    """Một thiết bị đã xuất hiện trong chính phiếu mượn đó."""
    def __init__(self, message):
        super().__init__(message)


class DeviceNotInSlipException(BorrowingException):
    """Yêu cầu trả thiết bị không thuộc phiếu."""
    def __init__(self, message):
        super().__init__(message)


class DeviceAlreadyReturnedException(BorrowingException):
    """Không được trả một thiết bị hai lần."""
    def __init__(self, message):
        super().__init__(message)


class InvalidReturnDateException(BorrowingException):
    """Ngày trả trước ngày mượn hoặc không có kiểu ngày hợp lệ."""
    def __init__(self, message):
        super().__init__(message)


class InvalidDeviceStateException(BorrowingException):
    """Chuyển trạng thái thiết bị không hợp lệ."""
    def __init__(self, message):
        super().__init__(message)