from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        StackedWidget.setObjectName("StackedWidget")
        StackedWidget.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StackedWidget.sizePolicy().hasHeightForWidth())
        StackedWidget.setSizePolicy(sizePolicy)
        StackedWidget.setMinimumSize(QtCore.QSize(640, 480))
        StackedWidget.setMaximumSize(QtCore.QSize(640, 480))
        self.page_startmenu = QtWidgets.QWidget()
        self.page_startmenu.setObjectName("page_startmenu")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.page_startmenu)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_startmenu = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_startmenu.setContentsMargins(0, 0, 0, 0)
        self.layout_startmenu.setObjectName("layout_startmenu")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_view = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_view.setMinimumSize(QtCore.QSize(0, 50))
        self.button_view.setMaximumSize(QtCore.QSize(300, 16777215))
        self.button_view.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_view.setStyleSheet("cursor: pointer;")
        self.button_view.setObjectName("button_view")
        self.horizontalLayout.addWidget(self.button_view)
        self.layout_startmenu.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_update_existing = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_update_existing.setMinimumSize(QtCore.QSize(0, 50))
        self.button_update_existing.setMaximumSize(QtCore.QSize(300, 16777215))
        self.button_update_existing.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_update_existing.setObjectName("button_update_existing")
        self.horizontalLayout_2.addWidget(self.button_update_existing)
        self.layout_startmenu.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_create_new = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_create_new.setMinimumSize(QtCore.QSize(0, 50))
        self.button_create_new.setMaximumSize(QtCore.QSize(300, 16777215))
        self.button_create_new.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.button_create_new.setObjectName("button_create_new")
        self.horizontalLayout_3.addWidget(self.button_create_new)
        self.layout_startmenu.addLayout(self.horizontalLayout_3)
        StackedWidget.addWidget(self.page_startmenu)
        self.page_create = QtWidgets.QWidget()
        self.page_create.setObjectName("page_create")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.page_create)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 641, 481))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pushButton)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pushButton_2)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.horizontalLayout_4.addLayout(self.formLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setMaximumSize(QtCore.QSize(160, 160))
        self.tableView.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        StackedWidget.addWidget(self.page_create)

        self.retranslateUi(StackedWidget)
        StackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

    def retranslateUi(self, StackedWidget):
        _translate = QtCore.QCoreApplication.translate
        StackedWidget.setWindowTitle(_translate("StackedWidget", "StackedWidget"))
        self.button_view.setText(_translate("StackedWidget", "PushButton"))
        self.button_update_existing.setText(_translate("StackedWidget", "PushButton"))
        self.button_create_new.setText(_translate("StackedWidget", "PushButton"))
        self.pushButton.setText(_translate("StackedWidget", "PushButton"))
        self.label.setText(_translate("StackedWidget", "TextLabel"))
        self.pushButton_2.setText(_translate("StackedWidget", "PushButton"))
        self.label_2.setText(_translate("StackedWidget", "TextLabel"))