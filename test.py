import unittest
from main import CategoryTree, Book, BOOKS, print_category_tree, read_data_from_file

class TestCategoryTree(unittest.TestCase):

    def setUp(self):
        """Thiết lập cây thể loại trước mỗi test case."""
        # Khởi tạo cây thể loại
        self.tree = CategoryTree()

    def test_add_books_to_tree(self):
        """Kiểm tra thêm sách từ BOOKS vào cây thể loại."""
        global BOOKS  # Sử dụng biến toàn cục BOOKS
        BOOKS.clear()  # Xóa dữ liệu cũ trong BOOKS
        BOOKS.extend(read_data_from_file("DanhSachBook.csv", "book"))  # Nạp dữ liệu mới vào BOOKS

        # Thêm tất cả sách từ BOOKS vào cây thể loại
        for book in BOOKS:
            print(f"Thêm sách '{book.title}' vào thể loại '{book.category}'")
            self.tree.add_book_to_category(book, book.category)

        # Kiểm tra các thể loại trong cây
        for book in BOOKS:
            category_node = self.tree.find_category(self.tree.root, book.category)
            self.assertIsNotNone(category_node)  # Đảm bảo thể loại tồn tại
            self.assertIn(book, category_node.books)  # Đảm bảo sách nằm trong thể loại

    def test_print_category_tree(self):
        """Kiểm tra hiển thị cây thể loại."""
        global BOOKS  # Sử dụng biến toàn cục BOOKS
        if not BOOKS:  # Nếu BOOKS chưa có dữ liệu, nạp dữ liệu từ file
            BOOKS.extend(read_data_from_file("DanhSachBook.csv", "book"))

        # Thêm tất cả sách từ BOOKS vào cây thể loại
        for book in BOOKS:
            self.tree.add_book_to_category(book, book.category)

        # Hiển thị cây
        print("\n--- Hiển thị cây thể loại ---")
        print_category_tree(self.tree.root)

if __name__ == "__main__":
    unittest.main()