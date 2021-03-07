# coding=utf-8

from ChessQLabel import ChessQLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os
import cv2

class ChessBoard():
    def __init__(self):
        self.chess_board_width = 700
        self.chess_board_height = 800
        self.chess_board_label = None
        self.chess_board_pic_name = 'qi_pan1.jpg'
        self.per_chessboard_width = 77
        self.per_chessboard_height = 77
        self.first_left_line = 0
        self.first_top_line = 0
        self.assert_dir = ''
        self.dialog_heigth = 0
        self.chess_board_map = []
        self.big_line_size = 4
        self.small_line_size = 2
        self.first_sub_chess_board_left = 0
        self.first_sub_chess_board_top = 0
        self.sub_chess_board_pic_rect = [] # [{}, {}, ...]

    def line_size_init(self, pic_width):
        temp_width = int(self.dialog_heigth / 10 * 9)
        self.big_line_size = int(self.big_line_size / temp_width * pic_width)
        self.small_line_size = int(self.small_line_size / temp_width * pic_width)

    def sub_chess_board_pic_rect_init(self, pic_file_path):
        sub_chess_board_handle = cv2.imread(pic_file_path)
        min_heigth = sub_chess_board_handle.shape[0]
        if int(sub_chess_board_handle.shape[1] / 9) < int(sub_chess_board_handle.shape[0] / 10):
            min_heigth = sub_chess_board_handle.shape[1]
        self.line_size_init(int(min_heigth / 10 * 9))
        for chess_board_idx in  range(90):
            row_idx = int(chess_board_idx / 9)
            col_idx = chess_board_idx % 9
            sub_chess_board_size = int((min_heigth - (2 * self.first_sub_chess_board_top)) / 10)
            left = self.first_sub_chess_board_left + col_idx * sub_chess_board_size
            top = self.first_sub_chess_board_top + row_idx * sub_chess_board_size
            rect = {'left': left, 'top': top, 'width': sub_chess_board_size, 'higth': sub_chess_board_size}
            dic_rect = {'rect': rect}
            self.sub_chess_board_pic_rect.append(dic_rect)

    def get_cut_sub_chess_board_pos(self, idx):
        '''
        :param idx:
        :return:返回每个子图的[x0,y0,x1,y1]
        '''
        x0 = self.sub_chess_board_pic_rect[idx]['rect']['left']
        y0 = self.sub_chess_board_pic_rect[idx]['rect']['top']
        x1 = x0 + self.sub_chess_board_pic_rect[idx]['rect']['width']
        y1 = y0 + self.sub_chess_board_pic_rect[idx]['rect']['higth']
        ret_rect = [x0, y0, x1, y1]
        return ret_rect

    def cut_and_save_sub_chess_board(self, chess_board_path):
        img = cv2.imread(chess_board_path)
        for i in range(90):
            rect = self.get_cut_sub_chess_board_pos(i)
            cropped = img[rect[1]:rect[3], rect[0]:rect[2]]  # 裁剪坐标为[y0:y1, x0:x1]
            cropped_new = self.draw_line_on_sub_chess_board(cropped, i)
            dst_pic_file = cv2.resize(cropped_new, (rect[3] - rect[1], rect[2] - rect[0]),
                                      interpolation=cv2.INTER_NEAREST)
            sub_chess_board_pic_name = 'sub_chess_board{}.jpg'.format(i)
            sub_chess_board_pic_path = os.path.join(self.assert_dir, sub_chess_board_pic_name)
            os.system('del {}'.format(sub_chess_board_pic_path))
            cv2.imwrite(sub_chess_board_pic_path, dst_pic_file)

    def create_sub_chess_board(self, chess_board_path):
        self.sub_chess_board_pic_rect_init(chess_board_path)
        # self.cut_and_save_sub_chess_board(chess_board_path)

    def draw_line(self, cropped, start_row, end_row, start_col, end_col):
        ret_pic = cropped
        ret_pic[start_row:end_row, start_col:end_col, 0] = 0
        ret_pic[start_row:end_row, start_col:end_col, 1] = 0
        ret_pic[start_row:end_row, start_col:end_col, 2] = 0
        return ret_pic

    def draw_top_left_sub_chess_board(self, cropped):
        ret_pic = cropped
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        end_row = row_num
        start_row = int(row_num / 2)
        start_col = int(col_num / 2) - self.big_line_size
        end_col = start_col + self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        end_row = int(row_num / 2)
        start_row = end_row - self.big_line_size
        start_col = int(col_num / 2) - self.big_line_size
        end_col = col_num
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_top_right_sub_chess_board(self, cropped):
        ret_pic = cropped
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        end_row = int(row_num / 2)
        start_row = end_row - self.big_line_size
        start_col = 0
        end_col = int(col_num / 2) + self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        end_row = row_num
        start_col = int(col_num / 2)
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_bottom_left_sub_chess_board(self, cropped):
        ret_pic = cropped
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = int(row_num / 2)
        end_row = start_row + self.big_line_size
        start_col = int(col_num / 2) - self.big_line_size
        end_col = col_num
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_row = 0
        end_row = int(col_num / 2) + self.big_line_size
        end_col = int(col_num / 2)
        start_col = end_col - self.big_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_bottom_right_sub_chess_board(self, cropped):
        ret_pic = cropped
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = 0
        end_row = int(row_num / 2) + self.big_line_size
        start_col = int(col_num / 2)
        end_col = start_col + self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_row = int(row_num / 2)
        end_row = start_row + self.big_line_size
        start_col = 0
        end_col = int(col_num / 2) + self.big_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_line_on_sub_chess_board(self, cropped, index):
        col_idx = index % 9
        ret_pic = cropped
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = 0
        end_row = row_num
        start_col = 0
        end_col = col_num
        if index == 0:
            return self.draw_top_left_sub_chess_board(cropped)
        if index == 8:
            return self.draw_top_right_sub_chess_board(cropped)
        if index == 81:
            return self.draw_bottom_left_sub_chess_board(cropped)
        if index == 89:
            return self.draw_bottom_right_sub_chess_board(cropped)
        if index < 9:
            end_row = int(row_num / 2)
            start_row = end_row - self.big_line_size
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
            end_row = row_num
            start_col = int(col_num / 2)
            end_col = start_col + self.small_line_size
        elif index >= 81:
            start_row = int(row_num / 2)
            end_row = start_row + self.big_line_size
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
            start_row = 0
            start_col = int(col_num / 2)
            end_col = start_col + self.small_line_size
        elif col_idx == 0:
            end_col = int(col_num / 2)
            start_col = end_col - self.big_line_size
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
            end_col = col_num
            start_row = int(row_num / 2)
            end_row = start_row + self.small_line_size
        elif col_idx == 8:
            start_col = int(col_num / 2)
            end_col = start_col + self.big_line_size
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
            start_col = 0
            start_row = int(row_num / 2)
            end_row = start_row + self.small_line_size
        else:
            start_col = int(col_num / 2)
            end_col = start_col + self.small_line_size
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
            start_col = 0
            end_col = col_num
            start_row = int(row_num / 2)
            end_row = start_row + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def chess_board_init(self, Dialog, dialog_heigth, chess_man_size, assert_dir, chess_obj_clicked):
        self.assert_dir = assert_dir
        self.dialog_heigth = dialog_heigth
        self.chess_board_label = ChessQLabel(Dialog)
        self.chess_board_label.set_chess_label_info('chess_board', 'chess_board')
        self.chess_board_label.setGeometry(QtCore.QRect(0, 0, self.chess_board_width, self.chess_board_height))
        chess_board_path = os.path.join(assert_dir, self.chess_board_pic_name)
        chess_board_pix = QPixmap(chess_board_path)
        pic_handle = chess_board_pix.scaled(self.chess_board_label.width(), self.chess_board_label.height())
        self.chess_board_label.setPixmap(pic_handle)
        self.chess_board_label.chess_lable_connect(chess_obj_clicked)
        self.create_chess_map(Dialog, dialog_heigth, chess_man_size)
        self.create_sub_chess_board(os.path.join(self.assert_dir, self.chess_board_pic_name))
        self.show_sub_chess_board(chess_obj_clicked)

    def get_sub_chess_board_rect(self, chess_board_idx, dialog_heigth):
        row_idx = int(chess_board_idx / 9)
        col_idx = chess_board_idx % 9
        sub_chess_board_size = int((dialog_heigth - (2 * self.first_sub_chess_board_top)) / 10)
        left = self.first_sub_chess_board_left + col_idx * sub_chess_board_size
        top = self.first_sub_chess_board_top + row_idx * sub_chess_board_size
        rect = {'left':left, 'top':top, 'width':sub_chess_board_size, 'higth':sub_chess_board_size}
        return rect

    def create_chess_map(self, Dialog, dialog_heigth, chess_man_size):
        # 棋盘10行9列
        half_chess_man_size = chess_man_size / 2
        self.per_chessboard_width = int(dialog_heigth / 10)
        self.per_chessboard_height = int(dialog_heigth / 10)
        for i in range(90):
            temp_row = int(i / 9)
            temp_col = i % 9
            x = self.first_left_line + temp_col * self.per_chessboard_width + int(self.per_chessboard_width / 2)\
                - half_chess_man_size
            y = self.first_top_line + temp_row * self.per_chessboard_height + int(self.per_chessboard_height / 2)\
                - half_chess_man_size
            poss_info = {}
            poss_info['x'] = x
            poss_info['y'] = y
            poss_info['sub_chess_board'] = {}
            poss_info['sub_chess_board']['rect'] = self.get_sub_chess_board_rect(i, dialog_heigth)
            poss_info['sub_chess_board']['label'] = ChessQLabel(Dialog)
            poss_info['chess_man'] = None
            self.chess_board_map.append(poss_info)

    def show_sub_chess_board(self, chess_obj_clicked):
        for i in range(90):
            sub_chess_board = self.chess_board_map[i]
            rect = sub_chess_board['sub_chess_board']['rect']
            sub_chess_board_label = sub_chess_board['sub_chess_board']['label']
            sub_chess_board_label.set_chess_label_info('sub_chess_board{}'.format(i), 'chess_board')
            sub_chess_board_label.setGeometry(QtCore.QRect(rect['left'], rect['top'], rect['width'], rect['higth']))
            sub_chess_board_pic_name = 'sub_chess_board{}.jpg'.format(i)
            chess_board_path = os.path.join(self.assert_dir, sub_chess_board_pic_name)
            chess_board_pix = QPixmap(chess_board_path)
            pic_handle = chess_board_pix.scaled(sub_chess_board_label.width(), sub_chess_board_label.height())
            sub_chess_board_label.setPixmap(pic_handle)
            sub_chess_board_label.chess_lable_connect(chess_obj_clicked)

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
