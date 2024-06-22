# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ScreenAddLocation.ui'
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
        self.buttonBack = QPushButton(Form)
        self.buttonBack.setObjectName(u"buttonBack")
        self.buttonBack.setGeometry(QRect(180, 170, 51, 23))
        font = QFont()
        font.setFamilies([u"Lucida Sans Unicode"])
        font.setPointSize(10)
        self.buttonBack.setFont(font)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(120, 70, 173, 43))
        self.label.setMinimumSize(QSize(173, 43))
        self.label.setMaximumSize(QSize(173, 43))
        font1 = QFont()
        font1.setFamilies([u"Lucida Sans Unicode"])
        font1.setPointSize(12)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEditCity = QLineEdit(Form)
        self.lineEditCity.setObjectName(u"lineEditCity")
        self.lineEditCity.setGeometry(QRect(150, 130, 113, 20))
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(11)
        self.lineEditCity.setFont(font2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.buttonBack.setText(QCoreApplication.translate("Form", u"Enter", None))
        self.label.setText(QCoreApplication.translate("Form", u"Enter a new Location", None))
        self.lineEditCity.setText("")
    # retranslateUi

