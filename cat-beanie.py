from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cat Beanie')

        self.file_name = ''
        
        self.toolbar = QToolBar(movable = False)

        self.folder_open = QAction('Open Folder',self)
        self.folder_open.triggered.connect(self.open_folder)
        self.toolbar.addAction(self.folder_open)
        
        self.font_sz_up = QAction('Font up',self)
        self.font_sz_up.triggered.connect(self.font_up)
        self.toolbar.addAction(self.font_sz_up)

        self.toolbar.addSeparator()

        self.font_sz_down = QAction('Font down',self)
        self.font_sz_down.triggered.connect(self.font_down)
        self.toolbar.addAction(self.font_sz_down)

        self.toolbar.addSeparator()
        
        font_select = QFontComboBox(currentFontChanged=self.change_font)
        self.toolbar.addWidget(font_select)

        self.toolbar.addSeparator()
        
        self.file_label = QLabel(f'File path: {self.file_name}')
        self.toolbar.addWidget(self.file_label)

        self.addToolBar(self.toolbar)

        self.text = QTextEdit()
        
        self.mfont = QFont()
        self.font_size = 11
        self.mfont.setPointSize(self.font_size)
        self.text.setFont(self.mfont)
        
        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.run_button = QPushButton("Run File")
        self.run_button.clicked.connect(self.run_file)
        
        master_layout = QVBoxLayout()

        self.nav_list = QTreeView()
        
        self.nav_list.clicked.connect(self.nav_item_change)

        self.text_layout = QHBoxLayout()
        self.text_layout.addWidget(self.nav_list, stretch = 1)
        self.text_layout.addWidget(self.text, stretch = 4)

        text_container = QWidget()
        text_container.setLayout(self.text_layout)

        master_layout.addWidget(text_container)
        
        button_layout = QHBoxLayout()
       # button_layout.addWidget(self.file_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.run_button)
        
        button_container = QWidget()
        button_container.setLayout(button_layout)
        
        master_layout.addWidget(button_container)

        container = QWidget()
        container.setLayout(master_layout)

        self.setCentralWidget(container)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectoryUrl(self, "Open a Folder")
        folder_name = folder.path()
    
        self.model = QFileSystemModel()
        self.model.setRootPath(folder_name)
        
        self.nav_list.setModel(self.model)
        self.nav_list.setRootIndex(self.model.index(folder_name))

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
        '/home/josephm/','All files (*.*)')
        
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

    def nav_item_change(self):
        try:
            self.file_name = self.model.filePath(self.nav_list.selectedIndexes()[0])
            print(self.file_name)

            with open(self.file_name, 'r') as file:
                self.text.setText(file.read())
        except IsADirectoryError or ValueError:
            pass


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    window = MainWindow()
    
    app.setStyleSheet("""
    QMainWindow {
        background-color: "dark-blue";
        color: "white";
        border: 2px;
        border-color: "dark-grey";
    }
    QPushButton {
        font-size: 16px;
        background-color: "navy";
        color: "white";
    }
    QTreeView {
        background-color: "grey";
    }
""")
    window.show()
    app.exec()
