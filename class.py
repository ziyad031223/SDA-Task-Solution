import json
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import sys

# Define a Book class to hold book information
class Book:
    def __init__(self, title, author, cost):
        self.__title = title
        self.__author = author
        self.__cost = cost
        
        
    def getTitle(self):
        return self.__title
    
    def getAuthor(self):
        return self.__author
    
    def getCost(self):
        return self.__cost


# Define a Section class to group books by sections
class Section:
    def __init__(self, title):
        self.__title = title
        self.__books = []


    def getTitle(self):
        return self.__title

    def addBook(self,book):
        self.__books.append(book)

    def searchBookByTitle(self, title):
        r_book = [book for book in self.__books if book.getTitle() == title]
        return r_book

    def searchBookByAuthor(self, author):
        r_book = [book for book in self.__books if book.getAuthor() == author]
        return r_book

    def deleteBook(self,title):
        self.__books = [book for book in self.__books if book.getTitle() != title]


    def showBooks(self):
        details_text=''
        for book in self.__books:
            details_text += f"Title: {book.getTitle()}\nAuthor: {book.getAuthor()}\nCost: {book.getCost()}\n"
        return details_text


# Define a Library class as a graphical interface using PyQt
class Library(qtw.QWidget):
    def __init__(self,title, json_file):
        super().__init__()
        
        # Load data from a JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        
        # Set up the main window
        self.setGeometry(300,300,800,800)
        self.setWindowTitle("Book store System")
        form_layout = qtw.QFormLayout()
        
        
        # Create UI elements
        self.setLayout(form_layout)
        label_0 = qtw.QLabel("View books")
        label_0.setFont(qtg.QFont("Helvetica", 24))
        label_1 = qtw.QLabel("Search a book")
        label_1.setFont(qtg.QFont("Helvetica", 24))
        t_name = qtw.QLineEdit(self)
        a_name = qtw.QLineEdit(self)
        details = qtw.QTextBrowser(self)
        details.setFont(qtg.QFont("Helvetica", 18))
        label_2 = qtw.QLabel("Buy a book")
        label_2.setFont(qtg.QFont("Helvetica", 24))
        b_name = qtw.QLineEdit(self)
        label_3 = qtw.QLabel("")
        label_3.setFont(qtg.QFont("Helvetica", 14))
        
        
        # Connect UI elements to corresponding functions
        form_layout.addRow(label_0)
        form_layout.addRow(qtw.QPushButton("view",clicked = lambda: press_it0()))
        form_layout.addRow(label_1)
        form_layout.addRow("Title", t_name)
        form_layout.addRow(qtw.QPushButton("Find by title",clicked = lambda: press_it1()))
        form_layout.addRow("Author", a_name)
        form_layout.addRow(qtw.QPushButton("Find by Author",clicked = lambda: press_it2()))
        form_layout.addRow(details)
        form_layout.addRow(label_2)
        form_layout.addRow("Title", b_name)
        form_layout.addRow(qtw.QPushButton("Buy",clicked = lambda: press_it3()))
        form_layout.addRow(label_3)
        
        self.show()
        
        
        def press_it0():
            self.showAllBooks()
            details.setText(f' {self.showAllBooks()}')
        def press_it1():
            details.setText(f' {self.searchBookByTitle(t_name.text())}')
        def press_it2():
            details.setText(f' {self.searchBookByAuthor(a_name.text())}')
        def press_it3():
            if self.sellaBook(b_name.text()):
                label_3.setText(f'successful !')
            else:
                label_3.setText(f'Book not found !')
        
        # Initialize library attributes
        self.__title = title
        self.__sections = []
        self.__profit = 0
        sections_data = {}
        for book_title, book_data in data.items():
            section_name = book_data["section"]
            if section_name not in sections_data:
                section = Section(section_name)
                self.__sections.append(section)
                sections_data[section_name] = section
            else:
                section = sections_data[section_name]
            book = Book(book_title, book_data["author"], book_data["cost"])
            section.addBook(book)
    
    
    def addSection(self,section):
        self.__sections.append(section)
    
    def searchBookByTitle(self, title):
        f_books = []
        for section in self.__sections:
            f_books.extend(section.searchBookByTitle(title))
            
        if f_books:
            details_text=''
            for book in f_books:
                details_text += f"Title: {book.getTitle()}\nAuthor: {book.getAuthor()}\nCost: {book.getCost()}\n\n"
            return details_text
        
        
    def searchBookByAuthor(self, author):
        f_books = []
        for section in self.__sections:
            f_books.extend(section.searchBookByAuthor(author))
        if f_books:
            details_text=''
            for book in f_books:
                details_text += f"Title: {book.getTitle()}\nAuthor: {book.getAuthor()}\nCost: {book.getCost()}\n\n"
            return details_text

    def showAllBooks(self):
        text=''
        for section in self.__sections:
            text+=section.getTitle()+' section : \n\n'+section.showBooks()+'\n\n'
        return text


    def getTotalProfit(self):
        return self.__profit

    def sellaBook(self, title):
        for section in self.__sections:
            found_books = section.searchBookByTitle(title)
            if found_books:
                for book in found_books:
                    self.__profit += book.getCost()
                    section.deleteBook(title)
                return True
        return False


def main():
    app = qtw.QApplication(sys.argv)
    library = Library('ziyad',"Z:/pic,vid/curl/books.json")
    library.showAllBooks()
    window = qtw.QMainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()