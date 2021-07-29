from os import walk, chdir
from os.path import getsize
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv, exit


class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setMinimumSize(QtCore.QSize(444, 222))
        MainWindow.setMaximumSize(QtCore.QSize(444, 222))

        self.central_widget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.central_widget)

        font = QtGui.QFont()
        font.setFamily('Verdana')
        font.setPointSize(9)
        font.setItalic(True)

        self.Input = QtWidgets.QLineEdit(self.central_widget)
        self.Input.setGeometry(QtCore.QRect(20, 40, 401, 41))
        self.Input.setFont(font)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 150, 421, 41))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(10)
        font.setItalic(False)

        self.SelectDirButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SelectDirButton.setFont(font)
        self.SelectDirButton.clicked.connect(self.get_directory)
        self.horizontalLayout.addWidget(self.SelectDirButton)

        self.StartButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StartButton.setFont(font)
        self.StartButton.clicked.connect(self.delete_meta)
        self.horizontalLayout.addWidget(self.StartButton)

        MainWindow.setWindowTitle('DeleteMeta')
        self.Input.setPlaceholderText('Путь к нужной папке')
        self.SelectDirButton.setText('Выбрать папку')
        self.StartButton.setText('Начать')

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_directory(self):
        dir_list = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку', '.')
        self.Input.setText(dir_list)

    def delete_meta(self):
        total_size = 0

        for root, _, files in walk(self.Input.text()):
            for file in files:
                if file.split('.')[-1].lower() in {'jpg', 'jpeg', 'img', 'png', 'bmp', 'ico'}:
                    full_path = f'{root}/{file}'
                    try:
                        total_size += getsize(full_path)
                        image = Image.open(full_path)
                        image.save(full_path)
                        total_size -= getsize(full_path)
                    except:
                        continue

        self.Input.setText(f'Завершено. Было сэкономлено {total_size//1048576} МБ.')


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    window = App()
    window.show()
    exit(app.exec_())
