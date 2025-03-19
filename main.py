# Lớp đại diện cho một cuốn sách
import csv
import time
class Book :
    def __init__(self, id, title, author, year, category, quantity):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.quantity = quantity
        
    def __str__(self):
        return f"{self.id} - {self.title} - {self.author} - {self.year} - {self.category} - {self.quantity}"

# Lớp đại diện cho một sinh viên
class Student:
    def __init__(self, id, name, class_name, faculty):
        self.id = id
        self.name = name
        self.class_name = class_name
        self.faculty = faculty

    def __str__(self):
        return f"{self.id} - {self.name} - {self.class_name} - {self.faculty}"

# Lớp đại diện cho một lần mượn sách
class BorrowRecord:
    def __init__(self, id, student_id, book_id, borrow_date, due_date):
        self.id = id
        self.student_id = student_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None
        self.status = "borrowed" 
    def __str__(self):
         return f"{self.id} - {self.student_id} - {self.book_id} - {self.borrow_date} - {self.due_date} - {self.status}"

STUDENS = []
# Đọc dữ liệu từ file Students.csv
with open("Students.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  

    for row in reader:
        stu = Student(*row)  
        STUDENS.append(stu)

BOOKS = []
# Đọc dữ liệu từ file Books.csv
with open("books.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  

    for row in reader:
        book = Book(*row)  
        BOOKS.append(book)
        
        
BORROW_RECORDS = []
# Đọc dữ liệu từ file borrow.csv
with open("borrow.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Bỏ qua dòng tiêu đề

    for row in reader:
        borrow_record = BorrowRecord(*row)
        BORROW_RECORDS.append(borrow_record)
#Helpers
def writeBooksToFile(newBook) :
    with open("books.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([newBook.id, newBook.title, newBook.author, newBook.year, newBook.category, newBook.quantity])
def saveBOOKSToFile(): 
    with open("books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Author", "Year", "Category", "Quantity"]) 
        for book in BOOKS:
            writer.writerow([book.id, book.title, book.author, book.year, book.category, book.quantity])               
#
#...
def add_student() :
    pass

def update_student() :
    pass

def delete_student() :
    pass 
#region book
def add_book() :
    global BOOKS  
    #ID,Title,Author,Year,Category,Quantity
    print("Điền các thông tin của cuốn sách mới thêm")
    ID = input("Nhập ID của sách : ")
    Title = input("Nhập Tên sách : ")
    Author = input("Nhập tên tác giả")
    Year = input("Nhập năm xuất bản")
    Category = input("Nhập thể loại")
    Quantity = input("Nhập số lượng")
    newBook = Book(ID,Title,Author,Year,Category,Quantity)
    BOOKS.append(newBook)
    writeBooksToFile(newBook)
    
#xóa sách theo ID 
def delete_book() : 
    global BOOKS  
    Book_ID = input("Nhập ID sách cần xóa :")
    for Books in BOOKS :
        if (Books.id == Book_ID) :
            print("Xóa sách :" + Books.title)
            BOOKS.remove(Books)
            saveBOOKSToFile()
            print("Xóa sách có ID: ",Book_ID)
            return
        else : print("Không có sách : " + Book_ID)
    
def update_book():
    book_id = input("Nhập ID của sách cần được sửa: ")
    for book in BOOKS:
        if book.id == book_id:
            print("Sửa sách :", book.title)
            print("Nếu không muốn thay đổi thông tin nào thì ấn Enter để qua thuộc tính tiếp theo")
            book.title = input(f"Tên sách ({book.title}): ") or book.title
            book.author = input(f"Tác giả ({book.author}): ") or book.author
            book.year = input(f"Năm xuất bản ({book.year}): ") or book.year
            book.category = input(f"Thể loại ({book.category}): ") or book.category
            book.quantity = input(f"Số lượng ({book.quantity}): ") or book.quantity
            saveBOOKSToFile()
            print("Sách đã được sửa")
            return
    print("Không tìm thấy sách có ID:", book_id)

            

#Giai đoạn 2 : 
def findBookByTitle() : 
    booktitle = input("Vui lòng nhập tên sách")
    for Books in BOOKS :
        if(Books.title == booktitle) :
            print(Books)

def findBookByAuthor():
    author_name = input("Vui lòng nhập tên tác giả")
    for Books in BOOKS :
        if(Books.Author == author_name) :
            print(Books)

def findBookByCategory() :
    Category = input("Vui lòng nhập thể loại")
    for Books in BOOKS :
        if(Books.category == Category) :
            print(Books)


#quicksort
def partition(array , low , high , key ):
    pivot = getattr(array[high],key)  #key là 1 trong 3 thuộc tính cần chọn
    i = low - 1
    
    for j in range(low,high) :
        if getattr(array[j],key) <= pivot :
            i += 1
            tmp = array[i]
            array[i] = array[j]
            array[j] = tmp
    
    tmp = array[i+1]
    array[i+1] = array[high]
    array[high] = tmp
    return i + 1
def quickSort(array , low , high , key) :
    if low < high :
        pivot = partition(array , low , high ,key)
        quickSort(array,low , pivot - 1 , key)
        quickSort(array ,pivot + 1 , high ,key)
#mergeSOrt
def mergeSort(books,key) :
    if len(books) <= 1 :
        return books
    mid = len(books) // 2
    left = mergeSort(books[:mid],key)
    right = mergeSort(books[mid:],key)
    
    return merge(left,right,key)

def merge(left,right,key) :
    tmpArray = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if getattr(left[i],key) <= getattr(right[j],key):
            tmpArray.append(left[i])
            i += 1
        else :
            tmpArray.append(right[j])
            j += 1
    
    tmpArray.extend(left[i:])
    tmpArray.extend(right[j:])
    return tmpArray
def inputSortBy() :
    sortBy = ["title", "author", "year"]
    
    while True:
        key = input("Nhập tiêu chí sắp xếp (title, author, year): ").strip().lower()
        if key in sortBy:
            return key
        print("Bạn vui lòng nhập lại đúng tiêu chí")

def quickSortBooks():
    global BOOKS
    sortBy = ["title", "author", "year"]
    key = inputSortBy()
    quickSort(BOOKS, 0, len(BOOKS) - 1, key)
    saveBOOKSToFile()
    print(f"Đã sắp xếp danh sách sách theo {key}")

def mergeSortBooks():   
    global BOOKS
    key = inputSortBy()
    BOOKS = mergeSort(BOOKS, key)
    saveBOOKSToFile()
    print(f"Đã sắp xếp danh sách sách theo {key}")

def Request3():
    global BOOKS
    key = inputSortBy()  
    
    quickSort = BOOKS[:]
    mergeSort = BOOKS[:]
    
    #quicksort time
    start_time = time.time()
    quickSort(quickSort, 0, len(quickSort) - 1, key)
    quick_time = time.time() - start_time

    #mergesort time
    start_time = time.time()
    sorted_books = mergeSort(mergeSort, key)
    merge_time = time.time() - start_time

    print(f"\n Kết quả so sánh sắp xếp theo '{key}':")
    print(f"Quick Sort: {quick_time:.6f} giây")
    print(f"Merge Sort: {merge_time:.6f} giây")

    if quick_time < merge_time:
        BOOKS = quickSort
    else:
        BOOKS = mergeSort

    saveBOOKSToFile()
#endregion
def main() :
    #TODO : add 10 student
    #TODO : update 1 students
    #TODO : add 5 books
    #TODO : update quantity of 2 books
    #TODO : Remove 1 book
    
    pass

if __name__ == "__main__" :
    main()