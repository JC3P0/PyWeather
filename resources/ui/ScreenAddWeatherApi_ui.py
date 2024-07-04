# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScreenAddWeatherApi.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(425, 275)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(425, 275))
        Form.setMaximumSize(QSize(425, 275))
        self.inputApi = QLineEdit(Form)
        self.inputApi.setObjectName(u"inputApi")
        self.inputApi.setGeometry(QRect(70, 119, 281, 21))
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setPointSize(11)
        self.inputApi.setFont(font)
        self.buttonSave = QPushButton(Form)
        self.buttonSave.setObjectName(u"buttonSave")
        self.buttonSave.setGeometry(QRect(180, 170, 61, 23))
        font1 = QFont()
        font1.setFamilies([u"Lucida Sans Unicode"])
        font1.setPointSize(10)
        self.buttonSave.setFont(font1)
        self.inputApiLabel = QLabel(Form)
        self.inputApiLabel.setObjectName(u"inputApiLabel")
        self.inputApiLabel.setGeometry(QRect(30, 50, 361, 51))
        font2 = QFont()
        font2.setFamilies([u"Lucida Sans Unicode"])
        font2.setPointSize(12)
        self.inputApiLabel.setFont(font2)
        self.inputApiLabel.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.inputApi.setText("")
        self.buttonSave.setText(QCoreApplication.translate("Form", u"Save", None))
        self.inputApiLabel.setText(QCoreApplication.translate("Form", u"Enter a valid free OpenWeatherMap API Key", None))
    # retranslateUi

