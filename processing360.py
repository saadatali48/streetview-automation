# -*- coding: utf-8 -*-



from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget
import os
from exif import Image 





qtCreatorFile = f"{os.getcwd()}{os.sep}code.ui"  # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(387, 238)
        MainWindow.setMinimumSize(QtCore.QSize(387, 238))
        MainWindow.setMaximumSize(QtCore.QSize(387, 238))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 90, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.browseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.browseBtn.setGeometry(QtCore.QRect(240, 90, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.browseBtn.setFont(font)
        self.browseBtn.setObjectName("browseBtn")
        self.processBtn = QtWidgets.QPushButton(self.centralwidget)
        self.processBtn.setGeometry(QtCore.QRect(270, 180, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        self.processBtn.setFont(font)
        self.processBtn.setObjectName("processBtn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process 360 Imagery"))
        self.label.setText(_translate("MainWindow", "Browse 360 Imagery folder"))
        self.browseBtn.setText(_translate("MainWindow", "Browse..."))
        self.processBtn.setText(_translate("MainWindow", "Process"))
        self.browseBtn.clicked.connect(self.BrowseFolder)
        self.processBtn.clicked.connect(self.Process360Imagery)

    def BrowseFolder(self):
        dlg = QtWidgets.QFileDialog()
        self.folder_path = dlg.getExistingDirectory(self, 'Select 360 Imagery directory')

    def Process360Imagery(self):
        for r, d, f in os.walk(self.folder_path):
            for file in f:
                if file.endswith(".jpg") or  file.endswith(".JPG"):
                    image_path = r + '/' + file
                    my_image = Image(image_path)
                    if my_image.has_exif:
                        lat = my_image.gps_latitude
                        lat = lat[0] + lat[1]/60 + lat[2]/3600 
                        lng = my_image.gps_longitude
                        lng = lng[0] + lng[1]/60 + lng[2]/3600
                        location=[lat,lng]
                        print(my_image.orientation)
                        scene_name = "scene_"+file.split(".")[0]
                        test = ImgTag(
                        filename=image_path,
                        force_case="lower",
                        strip=True,
                        no_duplicates=True)



                        self.PushDataToDb(scene_name, location)
                    else:
                        print(image_path + " has no Location data.")
                    # print(scene_name)
    def PushDataToDb(self, scene_name, latlng):
        pass

       


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
