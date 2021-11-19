from PyQt5 import QtCore, QtGui, QtWidgets
from sql import *

class Ui_Form_score_edit(object):
    def __init__(self, path):
        self.tabler = Tabler(path)

    def setupUi(self, Form_score_edit):   
        self.widget = Form_score_edit
        self.widget.setObjectName("Form_score_edit")
        self.widget.setFixedSize(400, 600)
        self.gridLayoutWidget = QtWidgets.QWidget(self.widget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 400, 600))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.layout_grid_scores = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.layout_grid_scores.setContentsMargins(0, 0, 0, 0)
        self.layout_grid_scores.setObjectName("layout_grid_scores")
        self.combobox_team2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combobox_team2.setObjectName("combobox_team2")
        self.layout_grid_scores.addWidget(self.combobox_team2, 0, 2, 1, 1)
        self.label_teams = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_teams.setObjectName("label_teams")
        self.layout_grid_scores.addWidget(self.label_teams, 0, 0, 1, 1)
        self.combobox_team1 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combobox_team1.setObjectName("combobox_team1")
        self.layout_grid_scores.addWidget(self.combobox_team1, 0, 1, 1, 1)
        self.layout_form_team1 = QtWidgets.QFormLayout()
        self.layout_form_team1.setObjectName("layout_form_team1")
        self.layout_grid_scores.addLayout(self.layout_form_team1, 1, 1, 1, 1)
        self.layout_form_team2 = QtWidgets.QFormLayout()
        self.layout_form_team2.setObjectName("layout_form_team2")
        self.layout_grid_scores.addLayout(self.layout_form_team2, 1, 2, 1, 1)
        self.label_scores = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_scores.setObjectName("label_scores")
        self.layout_grid_scores.addWidget(self.label_scores, 1, 0, 1, 1)
        self.button_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.button_save.setGeometry(QtCore.QRect(135, 565, 131, 32))
        self.button_save.setObjectName("button_save")
        self.form1_fields, self.form2_fields = [], []
        self.players_1, self.players_2 = [], []
        self.layout_grid_scores.addWidget(self.button_save, 2, 2, 1, 1)
        self.combobox_tour = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combobox_tour.setObjectName("combobox_tour")
        self.layout_grid_scores.addWidget(self.combobox_tour, 2, 0, 1, 1)

        self.teams = self.tabler.get_teams()

        for team in enumerate(self.teams):
            self.combobox_team1.addItem(team[1])
            self.combobox_team2.addItem(team[1])

        self.combobox_tour.currentIndexChanged.connect(lambda: self.load_players(0, self.combobox_tour.currentIndex()))
        self.combobox_tour.currentIndexChanged.connect(lambda: self.load_players(1, self.combobox_tour.currentIndex()))
        self.combobox_team1.currentIndexChanged.connect(lambda: self.load_players(0, 1))
        self.combobox_team2.currentIndexChanged.connect(lambda: self.load_players(1, 1))

        

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.widget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.widget.setWindowTitle(_translate("Form_score_edit", "Form"))
        self.label_teams.setText(_translate("Form_score_edit", "Команды:"))
        self.button_save.setText("Сохранить")
        self.label_scores.setText(_translate("Form_score_edit", "Очки:"))

    def load_players(self, combobox, tour):
        if combobox == 0:
            for i in reversed(range(self.layout_form_team1.count())): 
                self.layout_form_team1.itemAt(i).widget().deleteLater()
            self.players_1 = self.tabler.get_players(self.combobox_team1.currentIndex() + 1)

            self.form1_fields = list()
            for index, player in enumerate(self.players_1):
                self.form1_fields.append(QtWidgets.QSpinBox())
                self.form1_fields[index].setMaximum(200)
                self.form1_fields[index].setMinimum(-200)
                self.form1_fields[index].setValue(player[2 + self.combobox_tour.currentIndex() + 1])
                self.layout_form_team1.addRow(player[1] + ":", self.form1_fields[index])

        elif combobox == 1:
            for i in reversed(range(self.layout_form_team2.count())): 
                self.layout_form_team2.itemAt(i).widget().deleteLater()
            self.players_2 = self.tabler.get_players(self.combobox_team2.currentIndex() + 1)
            
            self.form2_fields = list()
            for index, player in enumerate(self.players_2):
                self.form2_fields.append(QtWidgets.QSpinBox())
                self.form2_fields[index].setMaximum(200)
                self.form2_fields[index].setMinimum(-200)
                self.form2_fields[index].setValue(player[2 + self.combobox_tour.currentIndex() + 1])
                self.layout_form_team2.addRow(player[1] + ":", self.form2_fields[index])

    def save(self):
        tour = self.combobox_tour.currentText().split()[1]

        if self.players_1[0][2] == self.players_2[0][2]:
            self.error_same_teams()
            return
        
        for player in self.players_1:
            score = self.form1_fields[self.players_1.index(player)].value()
            self.tabler.change_score(player[0], self.players_2[0][2], player[2], score, tour)

        for player in self.players_2:
            score = self.form2_fields[self.players_2.index(player)].value()
            self.tabler.change_score(player[0], self.players_1[0][2], player[2], score, tour)

        self.tabler.get_scores(tour)
        self.widget.close()

    def error_same_teams(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка")
        msg.setInformativeText('Команды не могут быть одинаковыми')
        msg.setWindowTitle("Ошибка")
        msg.exec_()




class Ui_Form_error(object):
    def __init__(self, error):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Form_score_edit()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())