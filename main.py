# coding=utf-8

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from ChessStrategy import ChessStrategy
from ChessCompetition import ChessCompetition
from ChessQLabel import ChessQLabel
from ChessBoard import ChessBoard
from ChessMan import ChessMan
import sys
import os
from pygame import mixer
import time
import threading

class Mp3Thread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.func = func

    def run(self):
        while not self.timeToQuit.isSet():
            self.func()
            self.timeToQuit.set()

class ChessWidget(QWidget):
    def set_close_call_back(self, func):
        self.close_call_back = func

    def closeEvent(self, event):
        result = QMessageBox.question(self, "中国象棋", "Do you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if (result == QMessageBox.Yes):
            self.close_call_back()
            time.sleep(1)
            event.accept()
        else:
            event.ignore()

class Ui_Dialog(QWidget):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.assert_dir = os.path.join(os.path.abspath('.'), 'assert')
        self.title_name = '中国象棋'
        self.chess_board_entry = None
        self.chess_man_entry = None
        self.dialog_heigth = 660
        self.dialog_width = int(self.dialog_heigth * 0.618 / 2) + self.dialog_heigth
        self.chess_man_size = int(self.dialog_heigth / 10 / 5 * 7)
        self.strategy_entry = ChessStrategy()
        self.competition = ChessCompetition()
        self.back_ground_label = None

    def chess_dub_player_thread(self):
        dub_mp3 = Mp3Thread(self.chess_dub_player)
        dub_mp3.start()

    def chess_dub_player(self):
        self.chess_dub_player_init()
        mixer.music.play()
        time.sleep(3)
        mixer.music.stop()

    def chess_dub_player_init(self):
        sound_file = os.path.join(self.assert_dir, 'chess.mp3')
        mixer.init()
        mixer.music.load(sound_file)

    def stop_all_thread(self):
        if self.chess_board_entry.chess_board_label.chess_thread != None:
            self.chess_board_entry.chess_board_label.chess_thread.kill_thread()
        for chess_name, value in self.chess_man_entry.chess_man_map.items():
            if value['label_handle'].chess_thread != None:
                value['label_handle'].chess_thread.kill_thread()

    def update_chess_man_method(self, chess_man):
        if chess_man['action'] == 'None':
            return True
        chess_man_handle = self.chess_man_entry.chess_man_map[chess_man['name']]
        if not chess_man_handle:
            return False
        pos = chess_man['pos']
        label_handle = chess_man_handle['label_handle']
        if chess_man['action'] == 'Del':
            if label_handle.chess_thread:
                label_handle.chess_thread.kill_thread()
            label_handle.setVisible(False)
            self.update_chess_map(pos, None)
            return True
        label_handle.setGeometry(QtCore.QRect(self.chess_board_entry.chess_board_map[pos]['x'],
                                              self.chess_board_entry.chess_board_map[pos]['y'],
                                              self.chess_man_size, self.chess_man_size))
        label_handle.setPixmap(chess_man_handle['pic_handle'])
        label_handle.setVisible(True)
        self.update_chess_map(pos, chess_man_handle)
        return True

    def update_chess_map(self, pos, chess_man):
        if chess_man != None:
            chess_man['pos'] = pos
            self.chess_man_entry.chess_man_map[chess_man['name']] = chess_man
        self.strategy_entry.chess_map[pos]['chess_man'] = chess_man

    def update_chess_man(self):
        if self.strategy_entry.update_first_chess_man['valid'] == True:
            if self.update_chess_man_method(self.strategy_entry.update_first_chess_man) != True:
                print('update_chess_man_method: first fail!!!')
                return
        if self.strategy_entry.update_second_chess_man['valid'] == True:
            if self.update_chess_man_method(self.strategy_entry.update_second_chess_man) != True:
                print('update_chess_man_method: second fail!!!')
                return
        if self.strategy_entry.update_third_chess_man['valid'] == True:
            if self.update_chess_man_method(self.strategy_entry.update_third_chess_man) != True:
                print('update_chess_man_method: third fail!!!')
        self.competition.change_cur_player()
        self.chess_dub_player_thread()

    def create_chess_man(self, Dialog):
        self.chess_man_entry = ChessMan(self.assert_dir, self.chess_man_size)
        self.chess_man_entry.chess_man_init(Dialog, self.chess_board_entry.set_chess_map_init_chess_man,
                                            self.chess_board_entry.get_position_by_pos,
                                            self.chess_obj_clicked)
        self.strategy_entry.set_chess_map(self.chess_board_entry.chess_board_map.copy())

    def is_exist_label_running_thread(self):
        for chess_name, value in self.chess_man_entry.chess_man_map.items():
            if not value['label_handle'].chess_thread:
                continue
            if value['label_handle'].chess_thread.is_alive():
                return True
        return False

    def chess_obj_clicked(self, name, type, index):
        chess_man_map = self.chess_man_entry.chess_man_map
        if self.is_exist_label_running_thread() != True:
            if type == 'chess_board':
                return False
            if self.competition.cur_player != chess_man_map[name]['color']:
                return False
            self.strategy_entry.last_click_entry['name'] = name
            return True
        else:
            if self.strategy_entry.last_click_entry['name'] == name:
                self.chess_man_entry.chess_man_map[name]['label_handle'].chess_thread.kill_thread()
                return False
            last_chess_man = chess_man_map[self.strategy_entry.last_click_entry['name']]
            cur_chess_man = None
            if type == 'chess_board':
                self.strategy_entry.second_click_info['chess_board_pos'] = index
            else:
                if last_chess_man['color'] == chess_man_map[name]['color']:
                    last_chess_man['label_handle'].chess_thread.kill_thread()
                    last_chess_man['label_handle'].setVisible(True)
                    self.strategy_entry.last_click_entry['name'] = name
                    return True
                cur_chess_man = chess_man_map[name]
                self.strategy_entry.second_click_info['chess_board_pos'] = 'None'
            self.strategy_entry.first_click_info['chess_man'] = last_chess_man
            self.strategy_entry.second_click_info['chess_man'] = cur_chess_man
            self.strategy_entry.strategy_run()
            return False

    def get_chess_board_entry(self):
        return self.chess_board_entry

    def strategy_entry_init(self):
        self.strategy_entry.chess_size_init(self.chess_man_size, self.chess_board_entry.chess_board_width,
                                            self.chess_board_entry.chess_board_height,
                                            self.chess_board_entry.per_chessboard_width,
                                            self.chess_board_entry.per_chessboard_height,
                                            self.chess_board_entry.first_left_line,
                                            self.chess_board_entry.first_top_line)
        self.strategy_entry.set_update_chess_man_func(self.update_chess_man)
        self.strategy_entry.set_chess_board_entry_func(self.get_chess_board_entry)

    def chess_board_create(self, Dialog):
        self.chess_board_entry = ChessBoard()
        self.chess_board_entry.chess_board_init(Dialog, self.dialog_heigth, self.chess_man_size,
                                                self.assert_dir, self.chess_obj_clicked)

    def back_ground_init(self, Dialog):
        self.back_ground_label = ChessQLabel(Dialog)
        self.back_ground_label.set_chess_label_info('back_ground', None)
        self.back_ground_label.setGeometry(QtCore.QRect(0, 0, self.dialog_width, self.dialog_heigth))
        back_ground_pix = QPixmap(os.path.join(self.assert_dir, 'back_ground.jpg'))
        pic_handle = back_ground_pix.scaled(self.back_ground_label.width(), self.back_ground_label.height())
        self.back_ground_label.setPixmap(pic_handle)

    def setupUi(self, Dialog):
        # 初始化顺序不可随意修改
        Dialog.setObjectName("Dialog")
        Dialog.resize(self.dialog_width, self.dialog_heigth)
        Dialog.set_close_call_back(self.stop_all_thread)
        self.chess_dub_player_init()
        self.back_ground_init(Dialog)
        self.chess_board_create(Dialog)
        self.create_chess_man(Dialog)
        self.strategy_entry_init()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", self.title_name))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = ChessWidget()
    mainwindow = Ui_Dialog()
    mainwindow.setupUi(main)
    main.setFixedSize(main.width(), main.height())
    # main.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)
    main.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)
    main.show()
    sys.exit(app.exec())
