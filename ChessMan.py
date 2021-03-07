# coding=utf-8

from ChessQLabel import ChessQLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os

class ChessMan():
    def __init__(self, assert_dir, chess_man_size):
        self.chess_man_size = chess_man_size # 108
        self.assert_dir = assert_dir
        self.chess_man_map = {}
        self.is_need_show_chess_man = True

    def chess_man_init(self, Dialog, set_chess_man_call_back_func, get_x_y_by_pos_call_back_func,
                       chess_obj_clicked_call_back_func):
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
                          {'label_handle': self.black_shuai, 'pos': 4, 'pic_name': 'black_shuai.png', 'name': 'black_shuai'},
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
                          {'label_handle': self.red_shuai, 'pos': 85, 'pic_name': 'red_shuai.png', 'name': 'red_shuai'},
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
        for chess_man_info in chess_man_info:
            self.set_chess_man(chess_man_info, set_chess_man_call_back_func, get_x_y_by_pos_call_back_func,
                               chess_obj_clicked_call_back_func)

    def set_chess_man(self, chess_man_info, set_chess_man_call_back_func, get_x_y_by_pos_call_back_func,
                      chess_obj_clicked_call_back_func):
        chess_man = chess_man_info['label_handle']
        pos = chess_man_info['pos']
        chess_man_name = chess_man_info['name']
        position = get_x_y_by_pos_call_back_func(pos)
        chess_man.setGeometry(QtCore.QRect(position[0], position[1], self.chess_man_size, self.chess_man_size))
        pix = QPixmap(os.path.join(self.assert_dir, chess_man_info['pic_name']))
        pic_handle = pix.scaled(self.chess_man_size, self.chess_man_size)
        if self.is_need_show_chess_man == True:
            chess_man.setPixmap(pic_handle)
        chess_man.set_chess_label_info(chess_man_name, 'chess_man')
        chess_man.chess_lable_connect(chess_obj_clicked_call_back_func)
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
        set_chess_man_call_back_func(pos, chess_man_info)
