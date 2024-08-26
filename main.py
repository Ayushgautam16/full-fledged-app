import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from ui_main import Ui_MainWindow
from ui_styles import Style
from ui_functions import *
import absl.logging
from PyQt5.QtCore import QLoggingCategory
from PyQt5.QtGui import QGuiApplication
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf.symbol_database')
absl.logging.set_verbosity(absl.logging.INFO)
absl.logging.use_python_logging()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self.setMaximumSize(QSize(1500, 900))

        #print('System: ' + platform.system())
        #print('Version: ' +platform.release())

        UIFunctions.removeTitleBar(True)
        self.setWindowTitle('Fitness AI Tracking & Instant Quantification')
        UIFunctions.labelTitle(self, 'Fitness AI Tracking & Instant Quantification')

        startSize = QSize(1000, 850)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "PUSH UP", "btn_pushup", "url(:/icons/train_icon.png)", True)
        UIFunctions.addNewMenu(self, "SQUAT", "btn_squat", "url(:/icons/train_icon.png)", True) 
        UIFunctions.addNewMenu(self, "SIT UP", "btn_situp", "url(:/icons/train_icon.png)", True)       
        UIFunctions.addNewMenu(self, "INFORMATION", "btn_info", "url(:/icons/info_icon.png)", True)   
          
        UIFunctions.selectStandardMenu(self, "btn_info")

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_info)

        UIFunctions.userIcon(self, "FATIQ", "", True)


        def moveWindow(event):
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)

        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
       
        self.show()
        

    def Button(self):
        btnWidget = self.sender()

        if btnWidget.objectName() == "btn_pushup":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_pushup)
            UIFunctions.resetStyle(self, "btn_pushup")
            UIFunctions.labelPage(self, "PUSH UP")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_squat":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_squat)
            UIFunctions.resetStyle(self, "btn_squat")
            UIFunctions.labelPage(self, "SQUAT")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_situp":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_situp)
            UIFunctions.resetStyle(self, "btn_situp")
            UIFunctions.labelPage(self, "SIT UP")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            
        if btnWidget.objectName() == "btn_info":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_info)
            UIFunctions.resetStyle(self, "btn_info")
            UIFunctions.labelPage(self, "Information")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        

       
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            #print("pos: ", event.pos())
            pass
   
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            #print('Mouse click: LEFT CLICK')
            pass
        if event.buttons() == Qt.RightButton:
            #print('Mouse click: RIGHT CLICK')
            pass
        if event.buttons() == Qt.MidButton:
            #print('Mouse click: MIDDLE BUTTON')
            pass
   

    def keyPressEvent(self, event):
        #print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
        pass
    
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        #print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())



