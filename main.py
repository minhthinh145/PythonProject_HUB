import csv
import time
import os

class Book:
    def __init__(self, id, title, author, year, category, quantity):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.quantity = int(quantity)
    def __str__(self):
        return f"{self.id} | {self.title} | {self.author} | {self.year} | {self.category} | {self.quantity}"

class Student:
    def __init__(self, id, name, class_name, faculty):
        self.id = id
        self.name = name
        self.class_name = class_name
        self.faculty = faculty

class BorrowRecord:
    def __init__(self, id, student_id, book_id, borrow_date, due_date):
        self.id = id
        self.student_id = student_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None
        self.status = "borrowed"  # borrowed, returned, overdue

def hien_thi_danh_sach_sach():
    if not BOOKS:
        print("Không có sách nào trong danh sách.")
        return

    print("\n--- DANH SÁCH SÁCH ---")
    print(f"{'ID':<6} {'Tiêu đề':<30} {'Tác giả':<20} {'Năm':<6} {'Thể loại':<15} {'Số lượng':<10}")
    print("-" * 90)
    for book in BOOKS:
        print(f"{book.id:<6} {book.title[:28]:<30} {book.author[:18]:<20} {book.year:<6} {book.category:<15} {book.quantity:<10}")

def hien_thi_danh_sach_sinh_vien():
    if not STUDENTS:
        print("Không có sinh viên nào trong danh sách.")
        return

    print("\n--- DANH SÁCH SINH VIÊN ---")
    print(f"{'ID':<6} {'Họ tên':<25} {'Lớp':<15} {'Khoa':<20}")
    print("-" * 70)
    for sv in STUDENTS:
        print(f"{sv.id:<6} {sv.name[:23]:<25} {sv.class_name:<15} {sv.faculty:<20}")

def hien_thi_danh_sach_muon_sach():
    if not BORROW_RECORDS:
        print("Không có bản ghi mượn sách nào.")
        return

    print("\n--- DANH SÁCH MƯỢN SÁCH ---")
    print(f"{'ID':<5} {'SV ID':<8} {'Sách ID':<8} {'Ngày mượn':<12} {'Hạn trả':<12} {'Ngày trả':<12} {'Trạng thái':<10}")
    print("-" * 80)
    for r in BORROW_RECORDS:
        print(f"{r.id:<5} {r.student_id:<8} {r.book_id:<8} {r.borrow_date:<12} {r.due_date:<12} {r.return_date or '':<12} {r.status:<10}")

#Đọc dữ liệu từ file
def read_data_from_file(filename, data_type):
    data = []
    if not os.path.exists(filename):
        return data

    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if data_type == "book":
                data.append(Book(
                id=row['id'], 
                title=row['title'], 
                author=row['author'], 
                year=row['year'], 
                category=row['category'], 
                quantity=int(row['quantity'])
            ))
            elif data_type == "student":
                data.append(Student(row["id"], row["name"], row["class_name"], row["faculty"]))
            elif data_type == "borrow_record":
                record = BorrowRecord(row["id"], row["student_id"], row["book_id"], row["borrow_date"], row["due_date"])
                record.return_date = row["return_date"] if row["return_date"] else None
                record.status = row["status"]
            
            elif data_type == "reservation":
                    data.append(Reservation(
                    student_id=row["student_id"],
                    book_id=row["book_id"],
                    reservation_date=row["reservation_date"]
                    ))
    return data

# Danh sách lưu trữ dữ liệu
BOOKS = read_data_from_file("DanhSachBook.cs", "book")
STUDENTS = read_data_from_file("students.csv", "student")
BORROW_RECORDS = read_data_from_file("borrowbooks.csv", "borrow_record")

# Thêm sách vào danh sách
def add_book(id, title, author, year, category, quantity):
    book = Book(id, title, author, year, category, quantity)
    BOOKS.append(book)

# Cập nhật số lượng sách theo id
def update_book_quantity(book_id, new_quantity):
    for book in BOOKS:
        if book.id == book_id:
            book.quantity = new_quantity
            print(f"Đã cập nhật số lượng sách '{book.title}' thành {new_quantity}.")
            return
    print("Không tìm thấy sách với ID đã cho.")

# Xóa sách theo id
def delete_book(book_id):
    global BOOKS
    BOOKS = [book for book in BOOKS if book.id != book_id]
    print(f"Đã xóa sách với ID {book_id}.")

def add_student(id, name, class_name, faculty):
    student = Student(id, name, class_name, faculty)
    STUDENTS.append(student)

# Cập nhật lớp hoặc khoa sinh viên theo ID
def update_student_info(student_id, new_class_name=None, new_faculty=None):
    for student in STUDENTS:
        if student.id == student_id:
            if new_class_name:
                student.class_name = new_class_name
            if new_faculty:
                student.faculty = new_faculty
            print(f"Đã cập nhật sinh viên '{student.name}' (ID: {student.id}).")
            return
    print("Không tìm thấy sinh viên với ID đã cho.")

# Xóa sinh viên theo ID
def delete_student(student_id):
    global STUDENTS
    STUDENTS = [student for student in STUDENTS if student.id != student_id]
    print(f"Đã xóa sinh viên với ID {student_id}.")

# Tìm kiếm sách 
def search_books(books, keyword, field_name):
    result = []
    keyword = keyword.lower().strip()

    for book in books:
        value = getattr(book, field_name).lower().strip()  
        if keyword == value or keyword in value.split():
            result.append(book)
    return result

# Tìm kiếm sách theo tiêu đề
def search_by_title(books, keyword):
    return search_books(books, keyword, "title")

# Tìm kiếm sách theo tác giả
def search_by_author(books, keyword):
    return search_books(books, keyword, "author")

# Tìm kiếm sách theo phân loạiloại
def search_by_category(books, keyword):
    return search_books(books, keyword, "category")

# Tìm kiếm sách theo tiêu chí kết hợphợp
def tim_ket_hop(books, tieu_de='', tac_gia='', phan_loai=''):
    ket_qua = []

    tieu_de = tieu_de.lower().strip()
    tac_gia = tac_gia.lower().strip()
    phan_loai = phan_loai.lower().strip()

    for book in books:
        match_title = True
        match_author = True
        match_category = True

        if tieu_de:
            title = book.title.lower()
            match_title = tieu_de in title and (
                tieu_de in title.split() or f" {tieu_de} " in f" {title} "
            )

        if tac_gia:
            author = book.author.lower()
            match_author = tac_gia in author and (
                tac_gia in author.split() or f" {tac_gia} " in f" {author} "
            )

        if phan_loai:
            category = book.category.lower()
            match_category = phan_loai in category and (
                phan_loai in category.split() or f" {phan_loai} " in f" {category} "
            )

        if match_title and match_author and match_category:
            ket_qua.append(book)

    return ket_qua
def hien_thi_sach(books):
    if not books:
        print("Không tìm thấy sách nào!")
        return

    print(f"{'ID':<5} {'Tên Sách':<30} {'Tác Giả':<20} {'Năm':<5} {'Thể Loại':<15} {'Số Lượng':<10}")
    print("=" * 110)

    for book in books:
        print(f"{book.id:<5} {book.title[:28]:<30} {book.author[:18]:<20} {book.year:<5} {book.category[:13]:<15}  {book.quantity:<10}")
#Định nghĩa Quicksort
def partition(array, low, high):
    pivot = array[high].title
    i = low - 1

    for j in range(low, high):
        if array[j].title <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

def sort_books_by_title_quick_sort(array, low, high):
    if low < high:
        pivot = partition(array, low, high)
        sort_books_by_title_quick_sort(array, low, pivot - 1)
        sort_books_by_title_quick_sort(array, pivot + 1, high)

#Định nghĩa Bubble Sort
def sort_books_by_title_bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j].title > array[j + 1].title:
                array[j], array[j + 1] = array[j + 1], array[j]

#So sánh thời gian thực thi giữa 2 thuật toán
def SoSanh():
    global BOOKS

    quickSortData = BOOKS[:]   # Dành cho quicksort
    bubbleSortData = BOOKS[:]  # Dành cho bubble sort

    # QuickSort Time
    start_time = time.time()
    sort_books_by_title_quick_sort(quickSortData, 0, len(quickSortData) - 1)
    quick_time = time.time() - start_time

    # BubbleSort Time
    start_time = time.time()
    sort_books_by_title_bubble_sort(bubbleSortData)
    bubble_time = time.time() - start_time

    print(f"\nKết quả so sánh sắp xếp theo 'title':")
    print(f"Quick Sort:  {quick_time:.6f} giây")
    print(f"Bubble Sort: {bubble_time:.6f} giây")

    # Gán BOOKS theo thuật toán nhanh hơn
    if quick_time < bubble_time:
        BOOKS = quickSortData
    else:
        BOOKS = bubbleSortData

def binary_search_books_by_title(books, keyword):
    keyword = keyword.lower().strip()
    result = []

    left, right = 0, len(books) - 1
    while left <= right:
        mid = (left + right) // 2
        mid_title = books[mid].title.lower().strip()

        if keyword == mid_title or keyword in mid_title.split():
            # Tìm thấy, mở rộng sang 2 bên
            result.append(books[mid])

            # Sang trái
            i = mid - 1
            while i >= 0:
                title = books[i].title.lower().strip()
                if keyword == title or keyword in title.split():
                    result.append(books[i])
                    i -= 1
                else:
                    break

            # Sang phải
            i = mid + 1
            while i < len(books):
                title = books[i].title.lower().strip()
                if keyword == title or keyword in title.split():
                    result.append(books[i])
                    i += 1
                else:
                    break
            break
        elif keyword < mid_title:
            right = mid - 1
        else:
            left = mid + 1

    return result

def compare_title_search(books, keyword):
    start_time = time.time()
    linear_result = search_by_title(books, keyword)
    linear_time = time.time() - start_time

    start_time = time.time()
    binary_result = binary_search_books_by_title(books, keyword)
    binary_time = time.time() - start_time

    print(f"[Tuyến tính] Thời gian: {linear_time:.6f}s, Kết quả: {len(linear_result)} cuốn")
    print(f"[Nhị phân]   Thời gian: {binary_time:.6f}s, Kết quả: {len(binary_result)} cuốn")

    return linear_result, binary_result

# Ghi lại dữ liệu mượn - trả vào file
def write_borrow_records_to_file(records, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "student_id", "book_id", "borrow_date", "due_date", "return_date", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow({
                "id": r.id,
                "student_id": r.student_id,
                "book_id": r.book_id,
                "borrow_date": r.borrow_date,
                "due_date": r.due_date,
                "return_date": r.return_date if r.return_date else "",
                "status": r.status
            })

def show_books_available_quantity():
    print("\n--- Danh sách sách còn lại ---")
    for book in BOOKS:
        if book.quantity > 0:
            print(f"{book.id} | {book.title} | Còn lại: {book.quantity}")

def show_books_quantity():
    print("\n--- Danh sách toàn bộ sách ---")
    for book in BOOKS:
        print(f"{book.id} | {book.title} | Số lượng: {book.quantity}")

def kiemTraSachConKhong():
    return all(book.quantity == 0 for book in BOOKS)

def inforStudent(student):
    print(f"Học sinh: {student.name} | Lớp: {student.class_name} | Khoa: {student.faculty}")

def tinhNgayHetHan(soNgay=3):
    return time.strftime("%Y-%m-%d", time.localtime(time.time() + soNgay * 86400))

def show_latest_30_borrow_records():
    records = sorted(BORROW_RECORDS, key=lambda x: x.borrow_date, reverse=True)[:30]
    print("\n--- 30 Latest Borrow Records ---")
    for r in records:
        print(r)

def borrowBook(student_id, book_id):
    global RESERVATION_QUEUE , STUDENTS, BOOKS, BORROW_RECORDS
    student = next((s for s in STUDENTS if s.id == student_id), None)
    if not student:
        print("Học sinh không tồn tại.")
        return

    book = next((b for b in BOOKS if b.id == book_id), None)
    if not book:
        print("Sách không tồn tại.")
        return

    if book.quantity <= 0:
        print("Sách này hiện tại không có sẵn.")
        return

    # Kiểm tra xem sách có trong hàng đợi không
    if not RESERVATION_QUEUE.is_empty():  # Nếu hàng đợi không trống
        for reservation in RESERVATION_QUEUE.queue:
            if reservation.book_id == book.id:
                if reservation.student_id == student.id:
                    # Nếu student_id trùng, xóa phần tử khỏi hàng đợi và cho phép mượn sách
                    RESERVATION_QUEUE.remove(reservation)
                    print(f"Đã cho sinh viên {student.name} mượn sách '{book.title}' từ hàng chờ.")
                    break
                else:
                    # Nếu student_id không trùng, báo rằng sách đang được ưu tiên cho sinh viên khác
                    print(f"Sách '{book.title}' đang được ưu tiên cho sinh viên khác.")
                    return
    else:
        # Nếu hàng đợi trống hoặc không có ai ưu tiên, cho phép mượn sách
        print(f"Hàng đợi trống hoặc không có ai ưu tiên. Cho phép sinh viên {student.name} mượn sách '{book.title}'.")

    # Nếu sách không có trong hàng đợi hoặc không có ai ưu tiên, cho mượn bình thường
    book.quantity -= 1

    # Tạo bản ghi mượn sách
    borrow_date = time.strftime("%Y-%m-%d")
    due_date = tinhNgayHetHan()
    new_id = str(int(BORROW_RECORDS[-1].id) + 1) if BORROW_RECORDS else "1"

    new_record = BorrowRecord(
        id=new_id,
        student_id=student.id,
        book_id=book.id,
        borrow_date=borrow_date,
        due_date=due_date
    )

    BORROW_RECORDS.append(new_record)
    write_borrow_records_to_file(BORROW_RECORDS, "borrowrecords.csv")

    # Thông báo
    print(f"Học sinh {student.name} đã mượn sách '{book.title}' thành công!")

    #Hiển thị thêm
    show_books_available_quantity()
    show_latest_30_borrow_records()
    
    
def search_borrow_history(student_id):
    global BORROW_RECORDS
    history = [r for r in BORROW_RECORDS if r.student_id == student_id]
    if not history:
        print("Không tìm thấy lịch sử mượn/trả sách của sinh viên này.")
        return

    print(f"\n--- LỊCH SỬ MƯỢN/TRẢ SÁCH CỦA SV {student_id} ---")
    print(f"{'ID':<4} {'Sách_ID':<8} {'Ngày mượn':<12} {'Hạn trả':<12} {'Ngày trả':<12} {'Trạng thái':<10}")
    print("-" * 65)
    for r in history:
        print(f"{r.id:<4} {r.book_id:<8} {r.borrow_date:<12} {r.due_date:<12} {r.return_date or '-':<12} {r.status:<10}")


def returnBook():
    global BORROW_RECORDS, BOOKS, STUDENTS

    student_id = input("Nhập ID của học sinh trả sách: ")
    student = next((s for s in STUDENTS if s.id == student_id), None)

    if student is None:
        print("Học sinh không tồn tại.")
        return

    book_id = input("Nhập ID của sách cần trả: ")
    book = next((b for b in BOOKS if b.id == book_id), None)

    if book is None:
        print("Sách không tồn tại.")
        return

    borrow_record = next(
        (r for r in BORROW_RECORDS if r.student_id == student_id and r.book_id == book_id and r.return_date is None),
        None
    )

    if borrow_record is None:
        print("Không tìm thấy bản ghi mượn sách hợp lệ.")
        return

    borrow_record.return_date = time.strftime("%Y-%m-%d")
    book.quantity += 1
    returnBook(borrow_record)  # Ghi vào danh sách trả

    print(f"Học sinh {student.name} đã trả sách '{book.title}' thành công! Số lượng hiện tại: {book.quantity}")
    notification_when_book_returned(book)

#Xác định và thông báo các trường hợp trả sách quá hạn
from datetime import datetime
def check_overdue_books():
    current_date = datetime.now()
    for record in BORROW_RECORDS:
        if record.return_date:
            return_dt = datetime.strptime(record.return_date, '%Y-%m-%d')
            borrow_dt = datetime.strptime(record.borrow_date, '%Y-%m-%d')
            if return_dt > borrow_dt and (return_dt - borrow_dt).days > 3:
                book = next((b for b in BOOKS if b.id == record.book_id), None)
                if book:
                    print(f"Sách '{book.title}' của sinh viên {record.student_id} đã trả quá hạn.")


def show_books_by_category():
    # Đếm số lượng sách theo từng thể loại
    dem_the_loai = Counter(book.category for book in BOOKS)

    print("Thống kê sách theo thể loại:")
    for the_loai, so_luong in dem_the_loai.items():
        print(f"{the_loai}: {so_luong} sách")
from collections import Counter
from datetime import datetime

def show_borrow_return_statistics():
    muon_theo_thang = Counter()
    tra_theo_thang = Counter()
    muon_theo_quy = Counter()
    tra_theo_quy = Counter()

    for record in BORROW_RECORDS:
        # Ngày mượn (định dạng yyyy-mm-dd)
        try:
            ngay_muon = datetime.strptime(str(record.borrow_date), '%Y-%m-%d')
            if record.status == "borrowed":
                thang = ngay_muon.strftime('%Y-%m')
                quy = (ngay_muon.month - 1) // 3 + 1
                quy_str = f"{ngay_muon.year}-Q{quy}"

                muon_theo_thang[thang] += 1
                muon_theo_quy[quy_str] += 1
        except:
            pass

        # Ngày trả (nếu có)
        if record.status == "returned" and record.return_date:
            try:
                ngay_tra = datetime.strptime(str(record.return_date), '%Y-%m-%d')
                thang = ngay_tra.strftime('%Y-%m')
                quy = (ngay_tra.month - 1) // 3 + 1
                quy_str = f"{ngay_tra.year}-Q{quy}"

                tra_theo_thang[thang] += 1
                tra_theo_quy[quy_str] += 1
            except:
                pass

    # In kết quả thống kê
    print("\nSố lần mượn sách theo tháng:")
    for thang, so_lan in sorted(muon_theo_thang.items()):
        print(f"{thang}: {so_lan} lượt mượn")

    print("\nSố lần trả sách theo tháng:")
    for thang, so_lan in sorted(tra_theo_thang.items()):
        print(f"{thang}: {so_lan} lượt trả")

    print("\nSố lần mượn sách theo quý:")
    for quy, so_lan in sorted(muon_theo_quy.items()):
        print(f"{quy}: {so_lan} lượt mượn")

    print("\nSố lần trả sách theo quý:")
    for quy, so_lan in sorted(tra_theo_quy.items()):
        print(f"{quy}: {so_lan} lượt trả")

from collections import Counter

def show_top_5_most_borrowed_books():
    # Đếm số lần mượn theo mã sách
    dem_muon = Counter(record.book_id for record in BORROW_RECORDS if record.status == "borrowed")
    top_5 = dem_muon.most_common(5)

    print("\nTop 5 cuốn sách được mượn nhiều nhất:")
    for book_id, so_lan in top_5:
        # Tìm thông tin sách từ mã sách
        book = next((b for b in BOOKS if b.id == book_id), None)
        if book:
            print(f"{book.title} (ID: {book.id}) - {so_lan} lượt mượn")
        else:
            print(f"Không tìm thấy thông tin sách có ID {book_id}")
def menu_quan_ly_sinh_vien():
    while True:
        print("""
        --- QUẢN LÝ SINH VIÊN ---
        1. Thêm sinh viên
        2. Cập nhật sinh viên
        3. Xóa sinh viên
        4. Hiển thị danh sinh viên
        0. Quay lại
        """)
        chon = input("Chọn chức năng: ")
        if chon == '1':
            so_sv = int(input("Bạn muốn thêm bao nhiêu sinh viên? "))
            for i in range(so_sv):
                print(f"\nNhập thông tin sinh viên thứ {i+1}:")
                sv_id = input("ID: ")
                name = input("Tên: ")
                class_name = input("Lớp: ")
                faculty = input("Khoa: ")
                add_student(sv_id, name, class_name, faculty)
        elif chon == '2':
            student_id = input("\nNhập ID sinh viên cần cập nhật: ")
            new_class = input("Nhập lớp mới: ")
            new_faculty = input("Nhập khoa mới: ")
            update_student_info(student_id, new_class_name=new_class, new_faculty=new_faculty)
        elif chon == '3':
            student_id = input("\nNhập ID sinh viên cần xóa: ")
            confirm = input(f"Bạn có chắc chắn muốn xóa sinh viên {student_id}? (y/n): ")
            if confirm.lower() == 'y':
                delete_student(student_id)
            else:
                print("Hủy thao tác xóa.")
        elif chon == '4':
            hien_thi_danh_sach_sinh_vien()
        elif chon == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")

def menu_quan_ly_sach():
    while True:
        print("""
        --- QUẢN LÝ SÁCH ---
        1. Thêm sách
        2. Cập nhật số lượng sách
        3. Xóa sách
        4. Hiển thị danh sách sáchsách
        0. Quay lại
        """)
        chon = input("Chọn chức năng: ")
        if chon == '1':
            so_sach = int(input("\nBạn muốn thêm bao nhiêu sách? "))
            for i in range(so_sach):
                print(f"\nNhập thông tin sách thứ {i+1}:")
                book_id = input("ID: ")
                title = input("Tên sách: ")
                author = input("Tác giả: ")
                year = int(input("Năm xuất bản: "))
                category = input("Thể loại: ")
                quantity = int(input("Số lượng: "))
                add_book(book_id, title, author, year, category, quantity)
        elif chon == '2':
            for _ in range(2):
                book_id = input("\nNhập ID sách cần cập nhật số lượng: ")
                try:
                    new_qty = int(input("Nhập số lượng mới: "))
                    update_book_quantity(book_id, new_qty)
                except ValueError:
                    print("Số lượng phải là số nguyên.")
        elif chon == '3':
            book_id = input("\nNhập ID sách cần xóa: ")
            confirm = input(f"Bạn có chắc chắn muốn xóa sách {book_id}? (y/n): ")
            if confirm.lower() == 'y':
                delete_book(book_id)
            else:
                print("Hủy thao tác xóa.")
        elif chon == '4':
            hien_thi_danh_sach_sach()
        elif chon == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")

def menu_tim_kiem_sach():
    while True:
        print("""
        --- TÌM KIẾM SÁCH ---
        1. Tìm theo tiêu đề
        2. Tìm theo tác giả
        3. Tìm theo thể loại
        4. Tìm theo nhiều tiêu chí
        0. Quay lại
        """)
        chon = input("Chọn chức năng: ")

        if chon == '1':
            keyword = input("Nhập tiêu đề sách cần tìm: ")
            ket_qua = search_by_title(BOOKS, keyword)
            hien_thi_sach(ket_qua)

        elif chon == '2':
            keyword = input("Nhập tên tác giả: ")
            ket_qua = search_by_author(BOOKS, keyword)
            hien_thi_sach(ket_qua)

        elif chon == '3':
            keyword = input("Nhập thể loại sách: ")
            ket_qua = search_by_category(BOOKS, keyword)
            hien_thi_sach(ket_qua)

        elif chon == '4':
            tieu_de = input("Nhập tiêu đề (có thể bỏ trống): ")
            tac_gia = input("Nhập tên tác giả (có thể bỏ trống): ")
            the_loai = input("Nhập thể loại (có thể bỏ trống): ")
            ket_qua = tim_ket_hop(BOOKS, tieu_de, tac_gia, the_loai)
            hien_thi_sach(ket_qua)

        elif chon == '0':
            break

        else:
            print("Lựa chọn không hợp lệ!")

def menu_muon_tra():
    while True:
        print("""
        --- QUẢN LÝ MƯỢN / TRẢ SÁCH ---
        1. Mượn sách
        2. Trả sách
        3. Xem sách còn lại
        4. Xem toàn bộ sách
        5. Hiển thị danh sách mượn sách
        0. Quay lại
        """)
        chon = input("Chọn chức năng: ")
        if chon == '1':         
            student_id = input("Nhập ID sinh viên mượn sách: ")
            book_id = input("Nhập ID sách muốn mượn: ")
            borrowBook(student_id, book_id)

        elif chon == '2':
            student_id = input("Nhập ID sinh viên trả sách: ")
            book_id = input("Nhập ID sách muốn trả: ")
            record = next((r for r in BORROW_RECORDS if r.student_id == student_id and r.book_id == book_id and r.return_date is None), None)
            if record:
                record.return_date = time.strftime("%Y-%m-%d")
                record.status = "returned"
                book = next((b for b in BOOKS if b.id == book_id), None)
                if book:
                    book.quantity += 1
                print(f"Đã trả sách thành công: SV {student_id} trả {book_id}")
            else:
                print("Không tìm thấy bản ghi mượn phù hợp.")
        elif chon == '3':
            show_books_available_quantity()
        elif chon == '4':
            show_books_quantity()
        elif chon == '5':
            hien_thi_danh_sach_muon_sach()
        elif chon == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")



def menu_thong_ke():
    while True:
        print("""
        --- THỐNG KÊ THƯ VIỆN ---
        1. Lịch sử mượn/trả theo sinh viên
        2. Kiểm tra sách trả quá hạn
        3. Thống kê sách theo thể loại
        4. Thống kê mượn/trả theo tháng & quý
        5. Top 5 sách được mượn nhiều nhất
        0. Quay lại
        """)
        chon = input("Chọn chức năng: ")
        if chon == '1':
            student_id = input("\nNhập ID sinh viên cần tra cứu lịch sử mượn/trả: ")
            search_borrow_history(student_id)
        elif chon == '2':
            check_overdue_books()
        elif chon == '3':
            show_books_by_category()
        elif chon == '4':
            show_borrow_return_statistics()
        elif chon == '5':
            show_top_5_most_borrowed_books()
        elif chon == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")

#region RESERVATION QUEUE
#tạo lớp ReservationQueue để triển khai cấu trúc queue
class Reservation:
    def __init__(self, student_id, book_id, reservation_date):
        self.student_id = student_id
        self.book_id = book_id
        self.reservation_date = reservation_date
        self.status = "reserved"  
        
    def __str__(self):
        return f"Reservation(student_id='{self.student_id}', book_id='{self.book_id}', reservation_date='{self.reservation_date}', status='{self.status}')"
    def __repr__(self):
        return self.__str__()
class ReservationQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, reservation: Reservation):
        self.queue.append(reservation)

    def dequeue(self) :
        if self.queue:
            return self.queue.pop(0)  # lấy người đầu tiên trong hàng chờ
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        return self.queue[0] if self.queue else None
    
    def remove(self, reservation: Reservation):
        if reservation in self.queue:
            self.queue.remove(reservation)
        else:
            print("Reservation không tồn tại trong hàng đợi.")
# Khởi tạo đối tượng ReservationQueue
RESERVATION_QUEUE = ReservationQueue()

# Đọc dữ liệu từ file và thêm vào hàng đợi
reservations = read_data_from_file("reservation.csv", "reservation")
for reservation in reservations:
    RESERVATION_QUEUE.enqueue(reservation)# Viết hàm đặt trước sách đang được mượn
def reserve_book(student_id, book_id):
    student = next((s for s in STUDENTS if s.id == student_id), None)
    if not student:
        print("Học sinh không tồn tại.")
        return

    book = next((b for b in BOOKS if b.id == book_id), None)
    if not book:
        print("Sách không tồn tại.")
        return

    if book.quantity > 0:
        borrowBook(student.id, book.id)  # gọi lại hàm mượn sách
    else:
        # Nếu sách không còn số lượng, thêm vào hàng chờ
        reservation_date = time.strftime("%Y-%m-%d")
        new_reservation = Reservation(student_id, book_id, reservation_date)
        RESERVATION_QUEUE.enqueue(new_reservation)

        print(f"Sách '{book.title}' hiện không có sẵn. Học sinh {student.name} đã được thêm vào danh sách chờ.")

#Viết hàm thông báo khi sách được trả về
def notification_when_book_returned(book_return):
    global RESERVATION_QUEUE, STUDENTS, BOOKS
    for queueBorrow in RESERVATION_QUEUE.queue:
        if queueBorrow.book_id == book_return.id:
            student = next((s for s in STUDENTS if s.id == queueBorrow.student_id), None)

            if student:
                print(f"Thông báo: Sách '{book_return.title}' đã được trả về. Học sinh {student.name} có thể đến mượn sách.")
            break
    
#endregion

#region CategoryNode _ CategoryTree
class CategoryNode:
    def __init__(self, name):
        self.name = name  # Tên của thể loại
        self.books = []   # Danh sách các sách trong thể loại này
        self.children = []  # Danh sách các thể loại con

    def add_book(self, book):
        self.books.append(book)

    def add_child(self, child_node):
        self.children.append(child_node)

# Lớp CategoryTree
class CategoryTree:
    def __init__(self):
        self.root = CategoryNode("Sách")

    #hàm này thêm sách vào category 
    def add_book_to_category(self, book, category_name):
        category_node = self.find_category(self.root, category_name)
        if category_node is None:
            category_node = CategoryNode(category_name)
            self.root.add_child(category_node)
        category_node.add_book(book)

    #Tìm xem category đã tồn tại trong cây chưa
    def find_category(self, node, category_name):
        """Tìm node thể loại theo tên (duyệt đệ quy)."""
        if node.name == category_name:
            return node
        for child in node.children:
            result = self.find_category(child, category_name)
            if result:
                return result
        return None

# Khởi tạo danh sách node Category từ danh sách sách
def init_category_nodes(books):
    category_map = {}
    for book in books:
        if book.category not in category_map:
            category_map[book.category] = CategoryNode(book.category)
        category_map[book.category].add_book(book)
    return list(category_map.values())

# In cây Category 
def print_category_tree(node, level=0, prefix=""):
    indent = "  " * level
    connector = "├── " if prefix else ""  # Ký tự nối
    print(f"{indent}{connector}{node.name}")

    for i, book in enumerate(node.books):
        book_connector = "│   " if i < len(node.books) - 1 else "    "
        print(f"{indent}  {book_connector}* {book.title} ({book.author}, {book.year}) - SL: {book.quantity}")

    for i, child in enumerate(node.children):
        child_prefix = "│   " if i < len(node.children) - 1 else "    "
        print_category_tree(child, level + 1, prefix=child_prefix)
        
# Khởi tạo danh sách CategoryNode từ danh sách sách
CATEGORY_NODES = init_category_nodes(BOOKS)
tree = CategoryTree()
# Thêm các node Category vào cây
for node in CATEGORY_NODES:
    tree.root.add_child(node)


#endregion
def main():
    while True:
        print("""
        === MENU CHÍNH ===
        1. Quản lý sinh viên
        2. Quản lý sách
        3. Quản lý mượn/trả sách
        4. Tìm kiếm sách
        5. Thống kê thư viện
        0. Thoát
        """)
        chon = input("Chọn chức năng: ")
        if chon == '1':
            menu_quan_ly_sinh_vien()
        elif chon == '2':
            menu_quan_ly_sach()
        elif chon == '3':
            menu_muon_tra()
        elif chon == '4':
            menu_tim_kiem_sach()
        elif chon == '5':
            menu_thong_ke()
        elif chon == '0':
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()

