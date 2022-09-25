from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os
import subprocess
import json

class ErrorMessage(QMainWindow):
    def __init__(self,parent=None):
        super(ErrorMessage,self).__init__(parent)
        self.label = QLabel()
        self.setCentralWidget(self.label)
    def showError(self,text):
        self.label.setText(text)
        self.show()

class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        os.chdir(os.path.dirname(__file__))
        self.current_directory = os.getcwd()
        self.setProperty("class", "thewindow")
        self.setWindowTitle('Cat Beanie')
        with open('config.json') as conf_file:
            configure = conf_file.read()
        self.config = json.loads(configure)
        
        if self.config["home_dir"] != '':
            self.home_dir = self.config["home_dir"]
        else:
            self.home_dir = os.path.expanduser('~')

        self.dir_path = os.path.dirname(os.path.abspath(__file__)) + '/directory'
        self.file_name = ''
        
        self.toolbar = QToolBar(movable = False)

        self.open_new_file = QAction('New File',self)
        self.open_new_file.triggered.connect(self.new_file)
        self.toolbar.addAction(self.open_new_file)
        self.toolbar.addSeparator()

        self.folder_open = QAction('Open Folder',self)
        self.folder_open.triggered.connect(self.open_folder)
        self.toolbar.addAction(self.folder_open)
        self.toolbar.addSeparator()

        self.home_change = QAction('Choose home directory',self)
        self.home_change.triggered.connect(self.choose_dir)
        self.toolbar.addAction(self.home_change)
        self.toolbar.addSeparator()
        
        self.file_label = QLabel(f'File path: {self.file_name}')
        self.toolbar.addWidget(self.file_label)

        self.addToolBar(self.toolbar)

        self.text = QTextEdit()

        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.run_button = QPushButton("Run File")
        self.run_button.clicked.connect(self.run_file)

        self.save_shortcut = QShortcut(QKeySequence('Ctrl+S'),self)
        self.save_shortcut.activated.connect(self.save_file)
        self.folder_shortcut = QShortcut(QKeySequence('Ctrl+Shift+F'),self)
        self.folder_shortcut.activated.connect(self.open_folder)
        
        self.nav_list = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(self.dir_path)
       
        self.nav_list.setModel(self.model)
        self.nav_list.setRootIndex(self.model.index(self.dir_path))     
        self.nav_list.clicked.connect(self.nav_item_change)

        self.terminal_directory = f"[{self.current_directory}]"
        self.terminal_text = self.terminal_directory
        self.terminal_output = QTextEdit()
        self.terminal_output.setText(self.terminal_text)
        self.terminal_output.setProperty("class","output")
        self.terminal_output.setReadOnly(True)

        self.output_layout = QVBoxLayout()
        self.output_layout.addWidget(self.text,stretch=3)
        self.output_layout.addWidget(self.terminal_output,stretch=2)
        
        self.output_container = QWidget()
        self.output_container.setLayout(self.output_layout)

        self.master_layout = QVBoxLayout()
        self.text_layout = QHBoxLayout()
        self.text_layout.addWidget(self.nav_list, stretch = 1)
        self.text_layout.addWidget(self.output_container, stretch = 4,)

        text_container = QWidget()
        text_container.setLayout(self.text_layout)
        self.master_layout.addWidget(text_container)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.run_button)
        
        button_container = QWidget()
        button_container.setLayout(button_layout)
        self.master_layout.addWidget(button_container)

        container = QWidget()
        container.setLayout(self.master_layout)
        self.setCentralWidget(container)
        self.show()
    def new_file(self):
        self.nav_list.clearSelection()
        self.text.clear()
        self.file_name == ''
    def open_folder(self):
        try:
            dest = QFileDialog.getExistingDirectoryUrl(self,'Open Folder')
            src = f'{self.dir_path}/{dest.fileName()}'
            if dest.path() == '':
                pass
            os.symlink(dest.path(), src)
        except Exception as e:
            self.message = ErrorMessage()
            self.message.showError(text = f'Error opening folder: {e}')
            pass
    def save_file(self):
        if self.file_name == '':
            self.save_as()
            return
        with open(self.file_name, "w") as new_file:
            new_file.write(self.text.toPlainText())
    def run_file(self):
            self.save_file()
            # TODO: replace with subprocess.popen this will allow it to run independently
            # in order to get the shit to work with popen i need to separate the terminal output 
            # update from the process call. i think
            process = subprocess.Popen([sys.executable,'-u',f'{self.file_name}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process_end = process.communicate()
            if process_end[0] != '':
                self.terminal_text += f"{process_end[0].decode('utf-8')}\n{self.terminal_directory}"
                self.terminal_output.setText(self.terminal_text)
    def save_as(self):
        new_name = QFileDialog.getSaveFileName(self, 'Save file as',
        self.home_dir,'All files (*.*)')
        if new_name[0] == '':
            return
        self.file_name = new_name[0]
        with open(self.file_name,'w') as file:
            file.write(str(self.text.toPlainText()))
    def choose_dir(self):
        new_dir = QFileDialog.getExistingDirectoryUrl(self,"Choose default directory")
        self.home_dir = new_dir.path()
        self.config["home_dir"] = new_dir.path()
        with open('config.json','w') as JSONfile:
            json.dump(self.config, JSONfile)
    def get_file_type(self):
        split_path = os.path.splitext(self.file_name)
        print(split_path[-1])
    def nav_item_change(self):
        try:
            file_info = self.nav_list.model().fileInfo(self.nav_list.selectedIndexes()[0])
            self.file_name = file_info.absoluteFilePath()
            self.file_label.setText(f'File path: {self.file_name}')
            with open(self.file_name, 'r') as file:
                self.text.setText(file.read())
        except IsADirectoryError:
            pass
        except Exception as e:
            self.message = ErrorMessage()
            self.message.showError(text = f'Error opening file: {e}')
            pass
if __name__ == '__main__':
    app =  QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet("""
    .thewindow {
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
    .output {
        background-color: "#363232";
        color: "white";
        border-color: "grey";
    }
""")
    app.exec()
