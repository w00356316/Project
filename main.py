# coding=utf-8

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from ChessStrategy import ChessStrategy
import sys
import os
import pyautogui as pag
import time
import math
import threading
import win32gui

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

class WorkerThread(threading.Thread):
    def __init__(self, func, wait_time):
        threading.Thread.__init__(self)
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.func = func
        self.wait_time = wait_time

    def kill_thread(self):
        self.timeToQuit.set()
        self.timeToQuit.wait(self.wait_time + 0.001)

    def run(self):
        while not self.timeToQuit.isSet():
            self.func()
            self.timeToQuit.wait(self.wait_time)

class ChessQLabel(QLabel):
    def __init__(self, parent=None):
        super(ChessQLabel, self).__init__(parent)
        self.name = ''
        self.thread_func = None
        self.click_call_back = None
        self.chess_thread = None

    def set_chess_label_name(self, name):
        self.name = name

    def mouseReleaseEvent(self, QMouseEvent):
        if self.click_call_back(self.name) != True:
            return
        if (self.chess_thread == None) or (not self.chess_thread.is_alive()):
            self.chess_thread = WorkerThread(self.thread_func, 0.35)
            self.chess_thread.start()
        else:
            self.chess_thread.kill_thread()
            self.setVisible(True)

    def chess_lable_connect(self, thread_func, click_func):
        self.thread_func = thread_func
        self.click_call_back = click_func

    def chess_board_clicked(self):
        if self.isVisible() == True:
            self.setVisible(False)
        else:
            self.setVisible(True)

class Ui_Dialog(QWidget):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.title_name = '中国象棋'
        self.chessboard_width = 700
        self.chessboard_height = 785
        self.per_chessboard_width = 77
        self.per_chessboard_height = 77
        self.chess_man_size = 108
        self.first_left_line = 44
        self.first_top_line = 48
        self.dialog_width = 880
        self.dialog_heigth = 800
        self.assert_dir = os.path.join(os.path.abspath('.'), 'assert')
        self.chess_map = []
        self.chess_man_map = {}
        self.strategy_entry = ChessStrategy()

    def stop_all_thread(self):
        if self.chessboard_lable.chess_thread != None:
            self.chessboard_lable.chess_thread.kill_thread()
        for chess_name, value in self.chess_man_map.items():
            if value['label_handle'].chess_thread != None:
                value['label_handle'].chess_thread.kill_thread()

    def update_chess_man_method(self, chess_man):
        if chess_man['action'] == 'None':
            return True
        chess_man_handle = self.chess_man_map[chess_man['name']]
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
        label_handle.setGeometry(QtCore.QRect(self.chess_map[pos]['x'], self.chess_map[pos]['y'], self.chess_man_size,
                                              self.chess_man_size))
        label_handle.setPixmap(chess_man_handle['pic_handle'])
        label_handle.setVisible(True)
        self.update_chess_map(pos, chess_man_handle)
        return True

    def update_chess_map(self, pos, chess_man):
        if chess_man != None:
            chess_man['pos'] = pos
            self.chess_man_map[chess_man['name']] = chess_man
        self.chess_map[pos]['chess_man'] = chess_man
        self.strategy_entry.set_chess_map(self.chess_map)

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

    def chess_man_init(self, Dialog):
        self.black_che_l = ChessQLabel(Dialog)
        self.black_ma_l = ChessQLabel(Dialog)
        self.black_xiang_l = ChessQLabel(Dialog)
        self.black_shi_l = ChessQLabel(Dialog)
        self.black_shuai = ChessQLabel(Dialog)
        self.black_shi_r = ChessQLabel(Dialog)
        self.black_xiang_r = ChessQLabel(Dialog)
        self.black_ma_r = ChessQLabel(Dialog)
        self.black_che_r = ChessQLabel(Dialog)
        self.black_pao_l = ChessQLabel(Dialog)
        self.black_pao_r = ChessQLabel(Dialog)
        self.black_bing1 = ChessQLabel(Dialog)
        self.black_bing2 = ChessQLabel(Dialog)
        self.black_bing3 = ChessQLabel(Dialog)
        self.black_bing4 = ChessQLabel(Dialog)
        self.black_bing5 = ChessQLabel(Dialog)
        self.red_che_l = ChessQLabel(Dialog)
        self.red_ma_l = ChessQLabel(Dialog)
        self.red_xiang_l = ChessQLabel(Dialog)
        self.red_shi_l = ChessQLabel(Dialog)
        self.red_shuai = ChessQLabel(Dialog)
        self.red_shi_r = ChessQLabel(Dialog)
        self.red_xiang_r = ChessQLabel(Dialog)
        self.red_ma_r = ChessQLabel(Dialog)
        self.red_che_r = ChessQLabel(Dialog)
        self.red_pao_l = ChessQLabel(Dialog)
        self.red_pao_r = ChessQLabel(Dialog)
        self.red_bing1 = ChessQLabel(Dialog)
        self.red_bing2 = ChessQLabel(Dialog)
        self.red_bing3 = ChessQLabel(Dialog)
        self.red_bing4 = ChessQLabel(Dialog)
        self.red_bing5 = ChessQLabel(Dialog)
        chess_man_info = [{'label_handle': self.black_che_l, 'pos': 0, 'pic_name': 'black_che.png', 'name': 'black_che_l'},
                          {'label_handle': self.black_ma_l, 'pos': 1, 'pic_name': 'black_ma.png', 'name': 'black_ma_l'},
                          {'label_handle': self.black_xiang_l, 'pos': 2, 'pic_name': 'black_xiang.png', 'name': 'black_xiang_l'},
                          {'label_handle': self.black_shi_l, 'pos': 3, 'pic_name': 'black_shi.png', 'name': 'black_shi_l'},
                          {'label_handle': self.black_shuai, 'pos': 4, 'pic_name': 'black_shuai.png', 'name': 'black_shuai_l'},
                          {'label_handle': self.black_shi_r, 'pos': 5, 'pic_name': 'black_shi.png', 'name': 'black_shi_r'},
                          {'label_handle': self.black_xiang_r, 'pos': 6, 'pic_name': 'black_xiang.png', 'name': 'black_xiang_r'},
                          {'label_handle': self.black_ma_r, 'pos': 7, 'pic_name': 'black_ma.png', 'name': 'black_ma_r'},
                          {'label_handle': self.black_che_r, 'pos': 8, 'pic_name': 'black_che.png', 'name': 'black_che_r'},
                          {'label_handle': self.black_pao_l, 'pos': 19, 'pic_name': 'black_pao.png', 'name': 'black_pao_l'},
                          {'label_handle': self.black_pao_r, 'pos': 25, 'pic_name': 'black_pao.png', 'name': 'black_pao_r'},
                          {'label_handle': self.black_bing1, 'pos': 27, 'pic_name': 'black_bing.png', 'name': 'black_bing1'},
                          {'label_handle': self.black_bing2, 'pos': 29, 'pic_name': 'black_bing.png', 'name': 'black_bing2'},
                          {'label_handle': self.black_bing3, 'pos': 31, 'pic_name': 'black_bing.png', 'name': 'black_bing3'},
                          {'label_handle': self.black_bing4, 'pos': 33, 'pic_name': 'black_bing.png', 'name': 'black_bing4'},
                          {'label_handle': self.black_bing5, 'pos': 35, 'pic_name': 'black_bing.png', 'name': 'black_bing5'},
                          {'label_handle': self.red_che_l, 'pos': 89, 'pic_name': 'red_che.png', 'name': 'red_che_l'},
                          {'label_handle': self.red_ma_l, 'pos': 88, 'pic_name': 'red_ma.png', 'name': 'red_ma_l'},
                          {'label_handle': self.red_xiang_l, 'pos': 87, 'pic_name': 'red_xiang.png', 'name': 'red_xiang_l'},
                          {'label_handle': self.red_shi_l, 'pos': 86, 'pic_name': 'red_shi.png', 'name': 'red_shi_l'},
                          {'label_handle': self.red_shuai, 'pos': 85, 'pic_name': 'red_shuai.png', 'name': 'red_shuai_l'},
                          {'label_handle': self.red_shi_r, 'pos': 84, 'pic_name': 'red_shi.png', 'name': 'red_shi_r'},
                          {'label_handle': self.red_xiang_r, 'pos': 83, 'pic_name': 'red_xiang.png', 'name': 'red_xiang_r'},
                          {'label_handle': self.red_ma_r, 'pos': 82, 'pic_name': 'red_ma.png', 'name': 'red_ma_r'},
                          {'label_handle': self.red_che_r, 'pos': 81, 'pic_name': 'red_che.png', 'name': 'red_che_r'},
                          {'label_handle': self.red_pao_l, 'pos': 64, 'pic_name': 'red_pao.png', 'name': 'red_pao_l'},
                          {'label_handle': self.red_pao_r, 'pos': 70, 'pic_name': 'red_pao.png', 'name': 'red_pao_r'},
                          {'label_handle': self.red_bing1, 'pos': 54, 'pic_name': 'red_bing.png', 'name': 'red_bing1'},
                          {'label_handle': self.red_bing2, 'pos': 56, 'pic_name': 'red_bing.png', 'name': 'red_bing2'},
                          {'label_handle': self.red_bing3, 'pos': 58, 'pic_name': 'red_bing.png', 'name': 'red_bing3'},
                          {'label_handle': self.red_bing4, 'pos': 60, 'pic_name': 'red_bing.png', 'name': 'red_bing4'},
                          {'label_handle': self.red_bing5, 'pos': 62, 'pic_name': 'red_bing.png', 'name': 'red_bing5'}]
        for chess_man in chess_man_info:
            self.set_chess_man(chess_man['label_handle'], chess_man['pos'], chess_man['pic_name'], chess_man['name'])

    def set_chess_man(self, chess_man, pos, pic_name, chess_man_name):
        chess_man.setGeometry(QtCore.QRect(self.chess_map[pos]['x'], self.chess_map[pos]['y'], self.chess_man_size,
                                           self.chess_man_size))
        pix = QPixmap(os.path.join(self.assert_dir, pic_name))
        pic_handle = pix.scaled(self.chess_man_size, self.chess_man_size)
        chess_man.setPixmap(pic_handle)
        chess_man.set_chess_label_name(chess_man_name)
        chess_man.chess_lable_connect(chess_man.chess_board_clicked, self.chess_obj_clicked)
        if not chess_man_name in self.chess_man_map:
            chess_man_info = {}
            chess_man_info['pos'] = pos
            chess_man_info['init_pos'] = pos
            chess_man_info['label_handle'] = chess_man
            chess_man_info['pic_handle'] = pic_handle
            chess_man_info['name'] = chess_man_name
            temp_color = 'black'
            if 'red' in chess_man_name:
                temp_color = 'red'
            chess_man_info['color'] = temp_color
            self.chess_man_map[chess_man_name] = chess_man_info
            self.chess_map[pos]['chess_man'] = chess_man_info

    def get_chess_board_pos(self):
        x, y = pag.position()
        win_handle = win32gui.FindWindow(None, self.title_name)
        left, top, right, bottom = win32gui.GetWindowRect(win_handle)
        left_pos = x - left - self.first_left_line
        top_pos = y - top - self.first_top_line
        # 棋盘10行9列
        row = round(top_pos / self.per_chessboard_height)
        if row > 0:
            row -= 1
        pos = row * 9
        pos += round(left_pos / self.per_chessboard_width)
        print('chess board click pos={}\n'.format(pos))  # 打印坐标
        return pos

    def is_exist_label_running_thread(self):
        for chess_name, value in self.chess_man_map.items():
            if not value['label_handle'].chess_thread:
                continue
            if value['label_handle'].chess_thread.is_alive():
                return True
        return False

    def chess_obj_clicked(self, name):
        if self.is_exist_label_running_thread() != True:
            if name == 'chess_board':
                return False
            self.strategy_entry.last_click_entry['name'] = name
            return True
        else:
            if self.strategy_entry.last_click_entry['name'] == name:
                self.chess_man_map[name]['label_handle'].chess_thread.kill_thread()
                return False
            last_chess_man = self.chess_man_map[self.strategy_entry.last_click_entry['name']]
            chess_man = None
            if name != 'chess_board':
                if last_chess_man['color'] == self.chess_man_map[name]['color']:
                    last_chess_man['label_handle'].chess_thread.kill_thread()
                    last_chess_man['label_handle'].setVisible(True)
                    self.strategy_entry.last_click_entry['name'] = name
                    return True
                chess_man = self.chess_man_map[name]
                self.strategy_entry.second_click_info['chess_board_pos'] = 'None'
            else:
                self.strategy_entry.second_click_info['chess_board_pos'] = self.get_chess_board_pos()
            self.strategy_entry.first_click_info['chess_man'] = last_chess_man
            self.strategy_entry.second_click_info['chess_man'] = chess_man
            self.strategy_entry.strategy_run()
            return False

    def chess_map_init(self):
        # 棋盘10行9列
        start_x = self.first_left_line + self.space
        start_y = self.first_top_line + self.space
        half_chess_man_size = self.chess_man_size / 2
        for i in range(90):
            temp_row = int(i / 9)
            temp_col = i % 9
            x = int(start_x + temp_col * self.per_chessboard_width - half_chess_man_size)
            y = int(start_y + temp_row * self.per_chessboard_height - half_chess_man_size)
            poss_info = {}
            poss_info['x'] = x
            poss_info['y'] = y
            poss_info['chess_man'] = None
            self.chess_map.append(poss_info)
        self.strategy_entry_init()

    def strategy_entry_init(self):
        self.strategy_entry.set_chess_map(self.chess_map)
        self.strategy_entry.chess_size_init(self.chess_man_size, self.chessboard_width, self.chessboard_height,
                                            self.per_chessboard_width, self.per_chessboard_height,
                                            self.first_left_line, self.first_top_line)
        self.strategy_entry.set_update_chess_man_func(self.update_chess_man)

    def chess_board_init(self, Dialog):
        self.chessboard_lable = ChessQLabel(Dialog)
        self.space = (self.dialog_heigth - self.chessboard_height) / 2
        self.chessboard_lable.setGeometry(QtCore.QRect(self.space, self.space, self.chessboard_width,
                                                       self.chessboard_height))
        chess_board_path = os.path.join(self.assert_dir, 'qi_pan.jpg')
        chess_board_pix = QPixmap(chess_board_path)
        pic_handle = chess_board_pix.scaled(self.chessboard_lable.width(), self.chessboard_lable.height())
        self.chessboard_lable.setPixmap(pic_handle)
        self.chessboard_lable.set_chess_label_name('chess_board')
        self.chessboard_lable.chess_lable_connect(self.chessboard_lable.chess_board_clicked, self.chess_obj_clicked)
        self.chess_board = {}
        self.chess_board['label_handle'] = self.chessboard_lable
        self.chess_board['pic_handle'] = pic_handle
        self.chess_board['name'] = 'chess_board'

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(self.dialog_width, self.dialog_heigth)
        Dialog.set_close_call_back(self.stop_all_thread)
        self.chess_board_init(Dialog)
        self.chess_map_init()
        self.chess_man_init(Dialog)
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
    main.show()
    sys.exit(app.exec())
