# -*- coding: utf-8 -*-
"""
@author: Mikel Val Calvo
@email: mvalcal1@upv.edu.es
@institution: Instituto Universitario de Investigación en Tecnología Centrada en el Ser Humano,
              Universitat Politècnica de València, València, Spain
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'M_GEERT_QT.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_M_GEERT(object):
    def setupUi(self, M_GEERT):
        M_GEERT.setObjectName("M_GEERT")
        M_GEERT.resize(1472, 922)
        self.centralwidget = QtWidgets.QWidget(M_GEERT)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.Experiment_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Experiment_btn.setObjectName("Experiment_btn")
        self.horizontalLayout_5.addWidget(self.Experiment_btn)
        self.MainRecord_btn = QtWidgets.QPushButton(self.centralwidget)
        self.MainRecord_btn.setObjectName("MainRecord_btn")
        self.horizontalLayout_5.addWidget(self.MainRecord_btn)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ResolveStreaming_btn = QtWidgets.QPushButton(self.groupBox)
        self.ResolveStreaming_btn.setObjectName("ResolveStreaming_btn")
        self.horizontalLayout_2.addWidget(self.ResolveStreaming_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.Activate_btn = QtWidgets.QPushButton(self.groupBox)
        self.Activate_btn.setObjectName("Activate_btn")
        self.horizontalLayout_2.addWidget(self.Activate_btn)
        self.Hide_btn = QtWidgets.QPushButton(self.groupBox)
        self.Hide_btn.setObjectName("Hide_btn")
        self.horizontalLayout_2.addWidget(self.Hide_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.Streamings_List = QtWidgets.QListWidget(self.groupBox)
        self.Streamings_List.setTabletTracking(False)
        self.Streamings_List.setProperty("isWrapping", False)
        self.Streamings_List.setSelectionRectVisible(True)
        self.Streamings_List.setObjectName("Streamings_List")
        self.verticalLayout_2.addWidget(self.Streamings_List)
        self.verticalLayout_11.addLayout(self.verticalLayout_2)
        self.verticalLayout_8.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TCPIP_checkBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.TCPIP_checkBox.setObjectName("TCPIP_checkBox")
        self.horizontalLayout.addWidget(self.TCPIP_checkBox)
        self.Host_LineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.Host_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Host_LineEdit.setObjectName("Host_LineEdit")
        self.horizontalLayout.addWidget(self.Host_LineEdit)
        self.Port_LineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        font = QtGui.QFont()
        font.setUnderline(False)
        self.Port_LineEdit.setFont(font)
        self.Port_LineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Port_LineEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Port_LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.Port_LineEdit.setObjectName("Port_LineEdit")
        self.horizontalLayout.addWidget(self.Port_LineEdit)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_8.addWidget(self.groupBox_4)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Run_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.Run_btn.setObjectName("Run_btn")
        self.horizontalLayout_3.addWidget(self.Run_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.Save_btn = QtWidgets.QPushButton(self.groupBox_2)
        self.Save_btn.setObjectName("Save_btn")
        self.horizontalLayout_3.addWidget(self.Save_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.Scripts_List = QtWidgets.QListWidget(self.groupBox_2)
        self.Scripts_List.setObjectName("Scripts_List")
        self.verticalLayout.addWidget(self.Scripts_List)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_8.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Logger = QtWidgets.QPlainTextEdit(self.groupBox_3)
        self.Logger.setObjectName("Logger")
        self.verticalLayout_3.addWidget(self.Logger)
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        self.verticalLayout_8.addWidget(self.groupBox_3)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout_8)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Code_TextEdit = QtWidgets.QPlainTextEdit(self.groupBox_5)
        self.Code_TextEdit.setObjectName("Code_TextEdit")
        self.verticalLayout_4.addWidget(self.Code_TextEdit)
        self.verticalLayout_9.addLayout(self.verticalLayout_4)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.groupBox_5)
        M_GEERT.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(M_GEERT)
        self.statusbar.setObjectName("statusbar")
        M_GEERT.setStatusBar(self.statusbar)

        self.retranslateUi(M_GEERT)
        QtCore.QMetaObject.connectSlotsByName(M_GEERT)

    def retranslateUi(self, M_GEERT):
        _translate = QtCore.QCoreApplication.translate
        M_GEERT.setWindowTitle(_translate("M_GEERT", "SIGNALINO"))
        self.Experiment_btn.setText(_translate("M_GEERT", "Experiment"))
        self.MainRecord_btn.setText(_translate("M_GEERT", "Record"))
        self.groupBox.setTitle(_translate("M_GEERT", "Lab Streaming Layer"))
        self.ResolveStreaming_btn.setText(_translate("M_GEERT", "Resolve Streaming"))
        self.Activate_btn.setText(_translate("M_GEERT", "Activate"))
        self.Hide_btn.setText(_translate("M_GEERT", "Hide"))
        self.groupBox_4.setTitle(_translate("M_GEERT", "TCP/IP Remote Control"))
        self.TCPIP_checkBox.setText(_translate("M_GEERT", "Trigger Server"))
        self.Host_LineEdit.setText(_translate("M_GEERT", "localhost"))
        self.Port_LineEdit.setText(_translate("M_GEERT", "10000"))
        self.groupBox_2.setTitle(_translate("M_GEERT", "Python Scripts"))
        self.Run_btn.setText(_translate("M_GEERT", "RUN"))
        self.Save_btn.setText(_translate("M_GEERT", "SAVE"))
        self.groupBox_3.setTitle(_translate("M_GEERT", "Log Viewer"))
        self.groupBox_5.setTitle(_translate("M_GEERT", "PYTHON RAW CODE"))
