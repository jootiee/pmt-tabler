from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_score_edit import *
from sql import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class Ui_Form(object):
    def __init__(self, Form):
        self.score_editor_widget = QtWidgets.QWidget()
        self.score_editor = Ui_Form_score_edit()
        self.score_editor.setupUi(self.score_editor_widget)
        self.tabler = Tabler()

        self.form = Form
        self.form.setObjectName("PMT Tabler")
        self.form.setFixedSize(800, 600)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout_4.setSizeConstraint(
            QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget_tables = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget_tables.setObjectName("tabWidget_tables")
        # self.tab_tables_1 = QtWidgets.QWidget()
        # self.tab_tables_1.setObjectName("tab_tables_1")
        # self.tabWidget_tables.addTab(self.tab_tables_1, "")
        self.horizontalLayout_2.addWidget(self.tabWidget_tables)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(15, 50, 15, 50)
        self.verticalLayout_3.setSpacing(25)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 50, -1, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.button_change_view = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.button_change_view.setObjectName("button_change_view")
        self.horizontalLayout.addWidget(self.button_change_view)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_edit_score = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.button_edit_score.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.button_edit_score)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
    
        self.tabs_tables = list()

        self.button_edit_score.clicked.connect(self.show_score_editor)

        self.score_editor.button_save.clicked.connect(lambda: self.score_editor.save(self.update_score))

        self.retranslateUi(self.form)
        QtCore.QMetaObject.connectSlotsByName(self.form)
        self.run()

    def run(self):
        self.path_table = QtWidgets.QFileDialog.getOpenFileName(
            self.form, 'Выбрать картинку', '', 'Таблица (*.db);;Таблица (*.db);;Все файлы (*)')[0]
        self.load_tables()
        self.load_tours()

    def load_tables(self):
        tours = self.tabler.get_tours()
        for tour in tours:
            # load of upper tables
            print(self.path_table)
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(self.path_table)
            db.open()

            view = QtWidgets.QTableView(self.form)
            view.verticalHeader().setVisible(False)
            view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            model = QSqlTableModel(self.form, db)
            model.setTable(tour)
            model.select()

            view.setModel(model)

            self.tabs_tables.append(view)
        
        view = QtWidgets.QTableView(self.form)

        model = QSqlTableModel(self.form, db)
        model.setTable("sessions")
        model.select()
        
        view.setModel(model)
        view.verticalHeader().setVisible(False)
        view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        view.setColumnHidden(0, True)

        self.verticalLayout.addWidget(view)
        view.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.verticalLayout.addWidget(self.button_edit_score)

    def load_tours(self):
        tours = self.tabler.get_tours()
        for index, tour in enumerate(tours):
            index_tour = "".join(list(filter(lambda x: x.isdigit(), tour)))
            self.tabWidget_tables.addTab(self.tabs_tables[index], "Тур " + index_tour)
            self.score_editor.combobox_tour.addItem("Тур " + index_tour)

    def update_score(self):
        pass
        teams = self.tabler.get_teams()
        players = self.tabler.get_players()

        for team in teams:
            for player in players:
                pass
                

    def show_score_editor(self):
        self.score_editor_widget.show()



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.tabWidget_tables.setTabText(self.tabWidget_tables.indexOf(self.tab_tables_1), _translate("Form", "Tab 1"))
        # self.tabWidget_tables.setTabText(self.tabWidget_tables.indexOf(self.tab_tables_2), _translate("Form", "Tab 2"))
        self.pushButton_2.setText(_translate("Form", "Настройка команд"))
        self.pushButton_3.setText(_translate("Form", "Новый тур"))
        self.pushButton_4.setText(_translate("Form", "Выход"))
        self.button_change_view.setText(_translate("Form", "Сохранить как..."))
        self.button_edit_score.setText(_translate("Form", "Настройка счета"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Form(Widget)
    Widget.show()
    sys.exit(app.exec_())
