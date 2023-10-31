from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_teams_edit(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(280, 400)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 280, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_add_player = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_add_player.setObjectName("button_add_player")
        self.verticalLayout.addWidget(self.button_add_player)
        self.button_edit_player = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_edit_player.setObjectName("button_edit_player")
        self.verticalLayout.addWidget(self.button_edit_player)
        self.button_delete_player = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_delete_player.setObjectName("button_delete_player")
        self.verticalLayout.addWidget(self.button_delete_player)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройка команд"))
        self.button_add_player.setText(_translate("Form", "Добавить игрока"))
        self.button_edit_player.setText(_translate("Form", "Изменить игрока"))
        self.button_delete_player.setText(_translate("Form", "Удалить игрока"))
