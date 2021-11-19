from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from sql import *
from Ui_score_edit import *
from Ui_team_edit import *
import sqlite3
import os

class App(object):
    def __init__(self, Form):
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
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 50, -1, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.button_edit_score = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.button_edit_score.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.button_edit_score)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.tabs_tables = list()

        self.retranslateUi(self.form)
        QtCore.QMetaObject.connectSlotsByName(self.form)
        self.path_table = QtWidgets.QFileDialog.getOpenFileName(self.form, 'Выбрать картинку', '', 'Таблица (*.db);;Таблица (*.db);;Все файлы (*)')[0]
        self.run()


    def run(self):
        self.score_editor_widget = QtWidgets.QWidget()
        self.score_editor = Ui_Form_score_edit(self.path_table)
        self.score_editor.setupUi(self.score_editor_widget)

        self.teams_editor_widget = QtWidgets.QWidget()
        self.teams_editor = Ui_Form_teams_edit()
        self.teams_editor.setupUi(self.teams_editor_widget)


        self.tabler = Tabler(self.path_table)



        self.button_edit_score.clicked.connect(self.show_score_editor)
        self.pushButton_2.clicked.connect(self.show_teams_editor)
        self.score_editor.button_save.clicked.connect(self.save_score)
        self.teams_editor.button_edit_player.clicked.connect(self.edit_player)
        self.teams_editor.button_add_player.clicked.connect(self.add_player)
        self.teams_editor.button_delete_player.clicked.connect(self.delete_player)
        self.pushButton_3.clicked.connect(self.new_tour)
        self.pushButton_4.clicked.connect(self.form.close)


        self.load_tables()
        self.load_tours()

    def save_score(self):
        self.score_editor.save()
        self.update_tables()

    def load_tables(self):
        tours = self.tabler.get_tours()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.path_table)
        self.db.open()

        for tour in tours:
            self.view1 = QtWidgets.QTableView(self.form)
            self.view1.verticalHeader().setVisible(False)
            self.view1.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)

            model = QSqlTableModel(self.form, self.db)
            model.setTable(tour)
            model.select()

            self.view1.setModel(model)

            self.tabs_tables.append(self.view1)

    def update_tables(self):
        tours = self.tabler.get_tours()
        for tab, tour, index in zip(self.tabs_tables, tours, range(len(tours))):
            model = QSqlTableModel(self.form, self.db)
            model.setTable(tour)
            model.select()
            tab.setModel(model)
            self.tabWidget_tables.removeTab(index)
            self.tabWidget_tables.addTab(
                tab, "Тур " + str(index + 1))

    def load_tours(self):
        tours = self.tabler.get_tours()
        try:
            for i in reversed(range(self.tabWidget_tables.count())):
                self.tabWidget_tables.removeTab(i)
        except Exception:
            pass
        

        for index, tour in enumerate(tours):
            index_tour = "".join(list(filter(lambda x: x.isdigit(), tour)))
            self.tabWidget_tables.addTab(
                self.tabs_tables[index], "Тур " + index_tour)
            self.score_editor.combobox_tour.addItem("Тур " + index_tour)

    def show_score_editor(self):
        tour = self.score_editor.combobox_tour.currentIndex()
        self.score_editor.load_players(0, tour)
        self.score_editor.load_players(1, tour)
        self.score_editor_widget.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "PMT Tabler"))
        # self.tabWidget_tables.setTabText(self.tabWidget_tables.indexOf(self.tab_tables_1), _translate("Form", "Tab 1"))
        # self.tabWidget_tables.setTabText(self.tabWidget_tables.indexOf(self.tab_tables_2), _translate("Form", "Tab 2"))
        self.pushButton_2.setText(_translate("Form", "Настройка команд"))
        self.pushButton_3.setText(_translate("Form", "Новый тур"))
        self.pushButton_4.setText(_translate("Form", "Выход"))
        # self.button_change_view.setText(_translate("Form", "Сохранить как..."))
        self.button_edit_score.setText(_translate("Form", "Настройка счета"))

    def new_tour(self):
        tours = self.tabler.get_tours()
        if tours:
            tours = sorted([int("".join(list(filter(lambda x: x.isdigit(), elem)))) for elem in tours])

            self.tabler.create_tour(tour=tours[-1] + 1)
        else:
            self.tabler.create_tour(tour=1)
        self.load_tours()
        self.update_tables()

    def edit_player(self):
        teams = self.tabler.get_teams()

        team, ok = QtWidgets.QInputDialog.getItem(self.form, 'Редактировать игрока', 'Выберите команду:', teams, 0, False)

        if team and ok:
            players = self.tabler.get_players(self.tabler.get_team_id(team))
            players_repr = [elem[1] for elem in players]
            player, ok = QtWidgets.QInputDialog.getItem(self.form, 'Редактировать игрока', 'Выберите игрока:', players_repr, 0, False)
            if player and ok:
                name, ok = QtWidgets.QInputDialog.getText(self.form, 'Редактирование команды', 'Введите новое имя:')
                if name and ok:
                    player = list(filter(lambda x: player == x[1], players))
                    self.tabler.edit_player(player[0][0], name)

    def add_player(self):
        teams = self.tabler.get_teams()

        team, ok = QtWidgets.QInputDialog.getItem(self.form, 'Добавление игрока', 'Выберите команду:', teams, 0, False)
        
        if team and ok:
            players = [elem[1] for elem in self.tabler.get_players(self.tabler.get_team_id(team))]
            name, ok = QtWidgets.QInputDialog.getText(self.form, 'Добавление игрока', 'Введите имя игрока:')
            if name and ok:
                if name in players:
                    self.error_player_exists()
                else:
                    self.tabler.add_player(name=name, team=team)

    def delete_player(self):
        teams = self.tabler.get_teams()

        team, ok = QtWidgets.QInputDialog.getItem(self.form, 'Удаление игрока', 'Выберите команду:', teams, 0, False)
        
        if team and ok:
            players = self.tabler.get_players(self.tabler.get_team_id(team))
            players_repr = [elem[1] for elem in self.tabler.get_players(self.tabler.get_team_id(team))]
            name, ok = QtWidgets.QInputDialog.getItem(self.form, 'Удаление игрока', 'Выберите игрока:', players_repr, 0, False)
            if name and ok:
                id = [elem[0] for elem in players if elem[1] == name][0]
                self.tabler.delete_player(id)
        
    def delete_team(self):
        teams = self.tabler.get_teams()
        team, ok =  QtWidgets.QInputDialog.getItem(self.form, "Удаление команды", "Выберите команду:", teams, 1, True)
        if team and ok:
            self.tabler.delete_team(self.tabler.get_team_id(team))
            self.update_tables()

    def error_team_exists(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Игрок с таким именем уже играет')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def error_in_progress(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Функция еще в разработке! :)')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def show_teams_editor(self):
        self.teams_editor_widget.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = App(Widget)
    Widget.show()
    sys.exit(app.exec_())
