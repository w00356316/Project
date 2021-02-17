# coding=utf-8

from ChessQLabel import ChessQLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os

class ChessBoard():
    def __init__(self):
        self.chess_board_width = 700
        self.chess_board_height = 800
        self.chess_board_label = None
        self.chess_board_pic_name = 'qi_pan.jpg'
        self.per_chessboard_width = 77
        self.per_chessboard_height = 77
        self.first_left_line = 44
        self.first_top_line = 55
        self.chess_board_map = []

    def chess_board_init(self, Dialog, dialog_heigth, chess_man_size, assert_dir, chess_obj_clicked):
        self.chess_board_label = ChessQLabel(Dialog)
        self.chess_board_label.set_chess_label_name('chess_board')
        self.chess_board_label.setGeometry(QtCore.QRect(0, 0, self.chess_board_width, self.chess_board_height))
        chess_board_path = os.path.join(assert_dir, self.chess_board_pic_name)
        chess_board_pix = QPixmap(chess_board_path)
        pic_handle = chess_board_pix.scaled(self.chess_board_label.width(), self.chess_board_label.height())
        self.chess_board_label.setPixmap(pic_handle)
        self.chess_board_label.chess_lable_connect(self.chess_board_label.chess_board_clicked, chess_obj_clicked)
        self.create_chess_map(dialog_heigth, chess_man_size)

    def create_chess_map(self, dialog_heigth, chess_man_size):
        # 棋盘10行9列
        start_x = self.first_left_line
        start_y = self.first_top_line
        half_chess_man_size = chess_man_size / 2
        for i in range(90):
            temp_row = int(i / 9)
            temp_col = i % 9
            x = int(start_x + temp_col * self.per_chessboard_width - half_chess_man_size)
            y = int(start_y + temp_row * self.per_chessboard_height - half_chess_man_size)
            poss_info = {}
            poss_info['x'] = x
            poss_info['y'] = y
            poss_info['chess_man'] = None
            self.chess_board_map.append(poss_info)

    def set_chess_map_init_chess_man(self, pos, chess_man):
        self.chess_board_map[pos]['chess_man'] = chess_man

    def get_position_by_pos(self, pos):
        rst = [0, 0]
        if pos >= 90:
            print('get_position_by_pos: pos({}) invalid!!!'.format(pos))
            return rst
        chess_man = self.chess_board_map[pos]
        rst[0] = chess_man['x']
        rst[1] = chess_man['y']
        return rst

    def get_pos_info_by_name(self, name):
        for chess_pos in self.chess_board_map:
            if chess_pos['chess_man'] != None:
                if chess_pos['chess_man']['name'] == name:
                    return chess_pos
        return None
