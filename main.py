import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QTabWidget, \
    QTableWidget, QTableWidgetItem, QDialog, QBoxLayout, QVBoxLayout, QComboBox
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")


        file_menu_item = self.menuBar().addMenu("&file")
        help_menu_item = self.menuBar().addMenu("&help")
        edit_menu_item = self.menuBar().addMenu("&edit")

        add_menu_student = QAction("Add Student", self)
        add_menu_student.triggered.connect(self.insert)
        file_menu_item.addAction(add_menu_student)

        add_help_student = QAction("About", self)
        help_menu_item.addAction(add_help_student)

        add_edit_student = QAction("Search", self)
        add_edit_student.triggered.connect(self.insert2)
        edit_menu_item.addAction(add_edit_student)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def insert2(self):
        dialog = Search()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Physics", "Chemistry", "Math", "English", "Geography", "History"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_number)

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)


        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        mainwindow.load_data()

class Search(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.highlight)
        layout.addWidget(button)

        self.setLayout(layout)

    def highlight(self):
        pass


app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec())