"""
/****************/
Mã sinh viên: 202419007
Họ tên: Phạm Anh Tú
/****************/


from datetime import date, datetime

from borrowers import Lecturer, TeachingAssistant
from borrowing import BorrowingSlip
from classroom import ClassRoom
from devices import AirConditionerRemote, ProjectorRemote, WirelessMicrophone
from maintenance import MaintenanceContract


def show_expected_error(title, expected_type, action):
    """Hàm phụ trợ để bắt lỗi và in ra kết quả cho sinh viên mới học."""
    print("  • " + title + ": ", end="")
    try:
        action()
    except expected_type as error:
        # Bắt đúng loại lỗi kỳ vọng
        print("PASS - " + str(error))
    except Exception as error:
        # Bắt nhầm loại lỗi khác
        print("FAIL - sai loại ngoại lệ: " + type(error).__name__ + " - " + str(error))
        raise
    else:
        # Nếu không có lỗi xảy ra như mong đợi
        print("FAIL - thao tác đáng lẽ phải bị từ chối")
        raise AssertionError(title)


def main():
    borrowed = datetime(2026, 10, 1, 8)
    lecturer = Lecturer("GV001", "Nguyễn Văn A")
    teaching_assistant = TeachingAssistant("TG001", "Trần Thị B")

    # Tạo các thiết bị dùng số thực hoặc số nguyên thay vì Decimal
    projector = ProjectorRemote("PRJ001", "Điều khiển máy chiếu", 2020, 1000000)
    ac = AirConditionerRemote("AC001", "Điều khiển điều hòa", 2019, 600000)
    microphone = WirelessMicrophone("MIC001", "Micro không dây", 2024, 1500000)
    
    # Cho điều hòa đi bảo trì
    ac.send_to_maintenance()

    # Tạo phòng học và thêm thiết bị vào
    classroom = ClassRoom("P301", "Phòng học P301", 60)
    classroom.add_device(projector)
    classroom.add_device(ac)
    classroom.add_device(microphone)

    print("=== LAB W06 - QUẢN LÝ THIẾT BỊ & PHIẾU MƯỢN ===")
    print("Phòng: " + classroom.room_name + " | Sức chứa: " + str(classroom.capacity))
    print("Chi phí bảo trì dự kiến/năm: " + str(classroom.calculate_annual_maintenance_cost()) + " VND")
    
    maintenance = classroom.get_devices_requiring_maintenance(date(2026, 10, 1))
    dev_ids = []
    for d in maintenance:
        dev_ids.append(d.device_id)
    print("Cần bảo trì: " + ", ".join(dev_ids))

    # Hợp đồng bảo trì
    contract = MaintenanceContract(
        "HD001", "Trung tâm bảo trì A", ac,
        date(2026, 1, 1), date(2026, 12, 31), 180000
    )
    is_act = contract.is_active(date(2026, 10, 1))
    print("Hợp đồng HD001 còn hiệu lực: " + str(is_act))

    print("\n[1] Luồng mượn/trả thành công")
    slip = BorrowingSlip("PM001", lecturer, classroom.room_id, borrowed)
    slip.add_device(projector, borrow_days=2, from_period=1, to_period=3)
    slip.add_device(microphone, borrow_days=1, from_period=1, to_period=2)
    
    item_ids = []
    for item in slip.items:
        item_ids.append(item.device.device_id)
    print("Thiết bị trên phiếu: " + ", ".join(item_ids))

    fee_projector = slip.return_device("PRJ001", datetime(2026, 10, 3, 8))
    fee_microphone = slip.return_device("MIC001", datetime(2026, 10, 4, 8))
    
    print("Phí trả máy chiếu đúng hạn: " + str(fee_projector) + " VND")
    print("Phí trả micro trễ 2 ngày: " + str(fee_microphone) + " VND")
    print("Tổng phí trễ trên PM001: " + str(slip.calculate_total_late_fee()) + " VND")

    # Tạo phiếu mượn thứ 2 để test danh sách chưa trả / quá hạn
    projector2 = ProjectorRemote("PRJ002", "Máy chiếu dự phòng", 2023, 900000)
    open_slip = BorrowingSlip("PM002", teaching_assistant, "P302", borrowed)
    open_slip.add_device(projector2, borrow_days=2)
    
    as_of = datetime(2026, 10, 5, 8)
    print("Phiếu chưa trả: " + open_slip.slip_id + " (" + str(len(open_slip.get_unreturned_items())) + " thiết bị)")
    print("Phiếu trễ chưa trả: " + open_slip.slip_id + " (" + str(len(open_slip.get_overdue_items(as_of))) + " thiết bị)")
    print("Phí phát sinh PM002 tới 05/10: " + str(open_slip.calculate_total_late_fee(as_of)) + " VND")

    print("\n[2] Các ca ngoại lệ bắt buộc")
    
    # 1. Thiết bị đang bảo trì nhưng đem đi mượn
    show_expected_error(
        "Thiết bị đang bảo trì", 
        Exception, 
        lambda: open_slip.add_device(ac, 1)
    )

    # 2. Trợ giảng mượn quá giới hạn (trợ giảng tối đa 2, thêm cái thứ 3)
    mic2 = WirelessMicrophone("MIC002", "Micro phụ", 2024, 600000)
    proj3 = ProjectorRemote("PRJ003", "Điều khiển phụ", 2024, 800000)
    open_slip.add_device(mic2, 1)
    
    show_expected_error(
        "Trợ giảng mượn thiết bị thứ ba", 
        Exception, 
        lambda: open_slip.add_device(proj3, 1)
    )

    # 3. Thêm trùng một thiết bị vào phiếu
    show_expected_error(
        "Thêm trùng một micro", 
        Exception, 
        lambda: slip.add_device(microphone, 1)
    )

    # 4. Micro vượt quá số ngày mượn quy định (Micro tối đa 1 ngày nhưng đòi mượn 3 ngày)
    show_expected_error(
        "Micro vượt 1 ngày", 
        Exception, 
        lambda: BorrowingSlip("PM003", lecturer, "P301", borrowed).add_device(microphone, 3)
    )

    # 5. Trả thiết bị không có trong phiếu
    show_expected_error(
        "Trả thiết bị ngoài phiếu", 
        Exception, 
        lambda: slip.return_device("PRJ999", datetime(2026, 10, 3))
    )

    # 6. Trả thiết bị đã trả rồi (trả 2 lần)
    show_expected_error(
        "Trả thiết bị hai lần", 
        Exception, 
        lambda: slip.return_device("MIC001", datetime(2026, 10, 5))
    )

    # 7. Ngày trả trước ngày mượn
    show_expected_error(
        "Ngày trả trước ngày mượn", 
        Exception, 
        lambda: open_slip.return_device("PRJ002", datetime(2026, 9, 30))
    )

    print("\n[3] Tính nhất quán")
    print("PM002 còn " + str(len(open_slip.items)) + " thiết bị; PRJ002 trạng thái = " + str(projector2.status))
    print("=== KẾT THÚC DEMO ===")


if __name__ == "__main__":
    main()