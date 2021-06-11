# -*- coding: utf-8 -*-
from os import walk, chdir
from os.path import getsize
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv, exit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setMinimumSize(QtCore.QSize(444, 222))
        MainWindow.setMaximumSize(QtCore.QSize(444, 222))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        font = QtGui.QFont()
        font.setFamily('Verdana')
        font.setPointSize(9)
        font.setItalic(True)

        self.Input = QtWidgets.QLineEdit(self.centralwidget)
        self.Input.setGeometry(QtCore.QRect(20, 40, 401, 41))
        self.Input.setFont(font)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 150, 421, 41))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(10)
        font.setItalic(False)

        self.SelectDirButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SelectDirButton.setFont(font)
        self.SelectDirButton.clicked.connect(self.getDirectory)
        self.horizontalLayout.addWidget(self.SelectDirButton)

        self.StartButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.StartButton.setFont(font)
        self.StartButton.clicked.connect(self.deleteMeta)
        self.horizontalLayout.addWidget(self.StartButton)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'DeleteMeta'))
        self.Input.setPlaceholderText(_translate('MainWindow', 'Путь к нужной папке'))
        self.SelectDirButton.setText(_translate('MainWindow', 'Выбрать папку'))
        self.StartButton.setText(_translate('MainWindow', 'Начать'))

    def getDirectory(self):
        dir_list = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку', '.')
        self.Input.setText(dir_list)

    def deleteMeta(self):
        directory = self.Input.text()
        chdir(directory)
        total_size = 0

        for root, _, files in walk(directory):
            for file in files:
                path = f'{root}/{file}'
                if file.title().split('.')[-1].lower() in ['jpg', 'jpeg', 'img', 'png']:
                    try:
                        total_size += getsize(path)
                        image = Image.open(path)
                        image.save(path)
                        total_size -= getsize(path)
                    except:
                        continue

        self.Input.setText(f'Завершено. Было сэкономлено {total_size//1048576} мегабайт.')


class App(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    window = App()
    window.show()
    exit(app.exec_())
