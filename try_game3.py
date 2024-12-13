import random
import Memory_cards
import SQL_Leader_board
import sqlite3
import os
import sys

from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QMainWindow, QPushButton, QWidget, QLabel, QTableWidget
from PyQt6 import QtGui
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHeaderView

from Class_cartochka import Cartochka
from Design_for_project import Ui_MainWindow


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pictures_name = [resource_path("dark_blue.jpeg"), resource_path("dark_pink.jpeg"), resource_path("green_image.png"),
                 resource_path("light_violet.png"), resource_path("orange.png"), resource_path("red_image.jpeg"),
                 resource_path("rose_image.png"), resource_path("violet_image.png"), resource_path("кофе2.jpeg")]


class Second(QMainWindow):
    def __init__(self):
        super().__init__()


class Memory_game(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_ui()

    def create_game_window(self):
        self.game_window.show()
        self.game_window.setWindowTitle("Игра")
        s = f"background-color: rgb({255}, {204}, {229});"
        self.game_window.setStyleSheet(s)
        self.game_window.setGeometry(100, 10, 600, 600)

    def create_choosing_color_window(self):
        self.choose_color_window.show()
        self.choose_color_window.setGeometry(100, 100, 400, 400)

    def create_winner_window(self):
        self.winner_window.show()
        self.winner_window.setWindowTitle("Завершение игры")
        s = f"background-image : url({resource_path('winning_image.jpeg')});"
        self.winner_window.setStyleSheet(s)
        self.winner_window.setGeometry(200, 200, 400, 400)

    def setup_ui(self):
        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle("Memory Game")

        self.leader_board = sqlite3.connect("leader_board.db")

        self.guessed_cards = []
        self.current_player = 1
        self.reversed_cards = []
        self.now_condition = 0

        self.game_window = Second()
        self.winner_window = Second()
        self.choose_color_window = Second()

        self.start_game_button.clicked.connect(self.create_game)
        self.show_players_button.clicked.connect(self.show_previous_players)
        self.player_name_edit.editingFinished.connect(self.add_new_player)

    def show_previous_players(self):
        cursor = self.leader_board.cursor()
        cursor.execute('SELECT username, guessed_cards, time FROM Users')
        results = cursor.fetchall()
        self.table_of_previous_players.setRowCount(len(results))
        self.table_of_previous_players.setColumnCount(3)
        self.table_of_previous_players.setHorizontalHeaderLabels(["Имя", "Отгад. карточки", "Время"])
        header = self.table_of_previous_players.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(len(results)):
            for j in range(3):
                self.table_of_previous_players.setItem(i, j, QTableWidgetItem(str(results[i][j])))
        self.table_of_previous_players.resizeColumnsToContents()
        self.leader_board.commit()

    def add_new_player(self):
        cursor = self.leader_board.cursor()
        cursor.execute('INSERT INTO Users (username, guessed_cards, time) VALUES (?, ?, ?)',
                       (self.player_name_edit.text(), 0, 0))
        self.leader_board.commit()

    def create_game(self):
        pole = self.choose_pictures_number.currentText()
        if pole == "4 на 4":
            self.board_width = 4
            self.board_height = 4
        if pole == "4 на 3":
            self.board_width = 4
            self.board_height = 3
        if pole == "3 на 4":
            self.board_width = 3
            self.board_height = 4
        if pole == "6 на 6":
            self.board_width = 6
            self.board_height = 6

        self.number_of_players = int(self.choose_number_of_players.currentText()[:1])
        self.guessed_cards = [0] * self.number_of_players

        self.create_game_window()
        self.create_game_board()

    def create_game_board(self):
        self.showing_time = self.choose_showing_time.text()
        if self.showing_time == "":
            self.showing_time = 2.5
        else:
            self.showing_time = int(self.showing_time)
        self.time_show = QLabel(self.game_window)
        self.show_time(0)
        self.time_show.resize(100, 20)
        self.time_show.move(self.board_width * (100 + 10) + 20, 20)
        self.time_show.show()
        self.create_Timer()

        self.current_player_widget = QLabel(self.game_window)
        self.show_current_player()
        self.current_player_widget.resize(120, 100)
        self.current_player_widget.move(self.board_width * (100 + 10) + 20, 100)
        self.current_player_widget.show()

        self.create_shuffle(self.board_width * self.board_height)

        self.playing_field_size = 500
        self.card_size = 0
        print(self.board_height, self.board_width)
        self.widget = QWidget(self.game_window)
        self.board = [
            [Cartochka(pictures_name[self.pict_numb[x * self.board_height + y]], x, y) for y in
             range(self.board_height)]
            for x in range(self.board_width)]
        for x in range(self.board_width):
            for y in range(self.board_height):
                cartochka = self.board[x][y]
                cartochka.setParent(self.widget)
                cartochka.setGeometry(x * 100 + 10 * x, y * 100 + 10 * y, 100, 100)
                cartochka.setIcon(QtGui.QIcon(resource_path("Обои.jpg")))
                cartochka.setIconSize(QtCore.QSize(100, 100))
                cartochka.clicked.connect(self.check_reversed_cards)
                cartochka.show()

        self.widget.resize(100 * self.board_width + 10 * (self.board_width - 1),
                           100 * self.board_height + 10 * (self.board_height - 1))
        self.widget.show()
        self.end_button = QPushButton(self.game_window)
        self.end_button.resize(100, 20)
        self.end_button.move(500, 500)
        self.end_button.show()
        self.end_button.clicked.connect(self.create_winner_window)
        self.end_button.clicked.connect(self.game_over)
        self.end_button.setText("Завершить игру")
        self.end_button.setStyleSheet("color: rgb(51, 0, 25);"
                                      "background-color: rgb(255, 102, 178);"
                                      "selection-color: rgb(51, 0, 25);"
                                      "selection-background-color: rgb(255, 0, 127);")

    def show_time(self, n):
        self.time_show.setText(f"Время: {n}")

    def create_Timer(self):
        time_value = int(self.time_show.text().split()[-1])
        if time_value < 600:
            self.show_time(time_value + 1)
            QTimer().singleShot(1000, self.create_Timer)
        else:
            self.game_over()

    def create_shuffle(self, n):
        mas = [i for i in range(0, n // 2) for _ in range(2)]
        random.shuffle(mas)
        print(mas)
        self.pict_numb = mas.copy()

    def check_reversed_cards(self):
        cartochka = self.sender()
        if cartochka.is_guessed:
            return
        if self.now_condition == 0:
            cartochka.choosed_first = True
            cartochka.reverse()
            self.reversed_cards.append(cartochka)
            self.now_condition = 1
        elif self.now_condition == 1:
            if not cartochka.choosed_first:
                self.now_condition = 2
                cartochka.reverse()
                self.reversed_cards.append(cartochka)
                QTimer().singleShot(int(self.showing_time * 1000), self.check_pair)

    def show_current_player(self):
        self.current_player_widget.setText("Ход игрока номер " + str(self.current_player))

    def check_pair(self):
        cartochka1 = self.reversed_cards[0]
        cartochka2 = self.reversed_cards[1]
        if cartochka1.picture_name == cartochka2.picture_name:
            cartochka1.is_guessed = True
            cartochka2.is_guessed = True
            self.guessed_cards[self.current_player - 1] += 2
            self.show_current_player()

            if sum(self.guessed_cards) == self.board_width * self.board_height:
                self.create_winner_window()
                self.game_over()

        else:
            cartochka1.choosed_first = False
            cartochka2.choosed_first = False
            cartochka1.reverse()
            cartochka2.reverse()
            self.current_player += 1
            if self.current_player > self.number_of_players:
                self.current_player = 1
            self.show_current_player()
        self.reversed_cards = []
        self.now_condition = 0

    def game_over(self):
        time_value = int(self.time_show.text().split()[-1])
        cursor = self.leader_board.cursor()
        cursor.execute('UPDATE Users SET guessed_cards = ?, time = ? WHERE username = ?',
                       (sum(self.guessed_cards), time_value, self.player_name_edit.text()))
        self.leader_board.commit()

        s = f"Время {time_value} секунды \n"
        max_, i_max = self.guessed_cards[0], [1]
        for i in range(self.number_of_players):
            if i != 0:
                if self.guessed_cards[i] > max_:
                    max_, i_max = self.guessed_cards[i], i + 1
                elif self.guessed_cards[i] == max_:
                    i_max.append(i + 1)
            s += f"Игрок №{i + 1} отгадал {self.guessed_cards[i]} карточек \n"
        if len(i_max) == 1:
            s += f"Победил игрок №{i_max[0]}"
        else:
            s += f"Победили игрки №{', '.join(i_max)}"
        self.information = QLabel(s, self.winner_window)
        self.information.show()
        self.information.move(100, 100)
        self.information.resize(200, 200)

        self.information.setStyleSheet("border: 2px rgb(153, 0, 76);"
                                       "border-radius: 4px;"
                                       "background: rgb(255, 192, 230);"
                                       "font: 10pt;")
        self.information.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leader_board.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = Memory_game()
    game.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())



"""
pyinstaller --onefile --windowed --add-data "Memory_cards:." --add-data "SQL_Leader_board.py:." --add-data 
"leader_board.db:." try_game3.py
"""
