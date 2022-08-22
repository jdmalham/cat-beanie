from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Text Editor')
        
        self.toolbar = QToolBar()
        font_select = QFontComboBox(currentFontChanged=self.change_font)
        
        self.font_sz_up = QAction('Font up',self)
        self.font_sz_up.triggered.connect(self.font_up)
        self.toolbar.addAction(self.font_sz_up)

        self.toolbar.addSeparator()

        self.font_sz_down = QAction('Font down',self)
        self.font_sz_down.triggered.connect(self.font_down)
        self.toolbar.addAction(self.font_sz_down)

        self.toolbar.addSeparator()
        
        self.toolbar.addWidget(font_select)

        self.file_name = ''
        
        self.text = QTextEdit()
        
        self.mfont = QFont()
        self.font_size = 11
        self.mfont.setPointSize(self.font_size)
        self.text.setFont(self.mfont)

        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)
        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.run_button = QPushButton("Run File")
        self.run_button.clicked.connect(self.run_file)
        
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.toolbar)
        master_layout.addWidget(self.text)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.run_button)
        
        button_container = QWidget()
        button_container.setLayout(button_layout)
        
        master_layout.addWidget(button_container)

        container = QWidget()
        container.setLayout(master_layout)

        self.setCentralWidget(container)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
        '/home/',"All files (*.*)")

        if fname[0] == '':
            return

        self.file_name = fname[0]
        
        with open(self.file_name, 'r') as file:
            self.text.setText(file.read())

    def save_file(self):
        if self.file_name == '':
            self.save_as()
            return
        
        with open(self.file_name, "w") as new_file:
            new_file.write(self.text.toPlainText())

    def run_file(self):
        self.save_file()
        os.system(f"python -u {self.file_name}")

    def change_font(self, font):
        self.mfont = QFont(font.key(), self.mfont.pointSize())
        self.text.setFont(self.mfont)

    def save_as(self):
        new_name = QFileDialog.getSaveFileName(self, 'Save file as',
        '/home/','All files (*.*)')
        
        if new_name[0] == '':
            return

        self.file_name = new_name[0]

        with open(self.file_name,'w') as file:
            file.write(str(self.text.toPlainText()))

    def font_up(self):
        point = self.mfont.pointSize()
        if point <= 39:
            self.mfont.setPointSize(point+1)
            self.text.setFont(self.mfont)

    def font_down(self):
        point = self.mfont.pointSize()
        if point > 1:
            self.mfont.setPointSize(point-1)
            self.text.setFont(self.mfont)


if __name__ == '__main__':

    app =  QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
