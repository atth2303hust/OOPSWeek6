/****************/
Mã sinh viên: 202419007
Họ tên: Phạm Anh Tú
/****************/

from abc import ABC, abstractmethod

# Lớp trừu tượng (Giao diện) cho người mượn
class IBorrower(ABC):
    def __init__(self, borrower_id, full_name):
        self.borrower_id = borrower_id
        self.full_name = full_name

    @abstractmethod
    def get_maximum_devices(self):
        pass


# Lớp Giảng viên kế thừa từ IBorrower
class Lecturer(IBorrower):
    def __init__(self, borrower_id, full_name):
        super().__init__(borrower_id, full_name)

    def get_maximum_devices(self):
        return 3


# Lớp Trợ giảng kế thừa từ IBorrower
class TeachingAssistant(IBorrower):
    def __init__(self, borrower_id, full_name):
        super().__init__(borrower_id, full_name)

    def get_maximum_devices(self):
        return 2