# coding=utf-8

from ChessQLabel import ChessQLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os
import cv2
import math

class ChessBoard():
    def __init__(self):
        self.chess_board_width = 700
        self.chess_board_height = 800
        self.chess_board_label = None
        self.chess_board_pic_name = 'qi_pan1.jpg'
        self.is_need_save_sub_chess_board = False
        self.pao_and_bing_flag_len = 8
        self.per_chessboard_width = 77
        self.per_chessboard_height = 77
        self.first_left_line = 0
        self.first_top_line = 0
        self.assert_dir = ''
        self.dialog_heigth = 0
        self.chess_board_map = []
        self.big_line_size = 5
        self.small_line_size = 3
        self.line_color = {'R':20, 'G':40, 'B':80}
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
        if self.is_need_save_sub_chess_board == True:
            self.cut_and_save_sub_chess_board(chess_board_path)

    def draw_line(self, cropped, start_row, end_row, start_col, end_col):
        ret_pic = cropped
        temp_end_row = cropped.shape[0] - 1
        if end_row < temp_end_row:
            temp_end_row = end_row
        temp_end_col = cropped.shape[1] - 1
        if end_col < temp_end_col:
            temp_end_col = end_col
        ret_pic[start_row:temp_end_row, start_col:temp_end_col, 2] = self.line_color['R']
        ret_pic[start_row:temp_end_row, start_col:temp_end_col, 1] = self.line_color['G']
        ret_pic[start_row:temp_end_row, start_col:temp_end_col, 0] = self.line_color['B']
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

    def draw_top_row_sub_chess_board(self, cropped, index):
        ret_pic = self.check_and_draw_shi_line(cropped, index)
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        end_row = int(row_num / 2)
        start_row = end_row - self.big_line_size
        start_col = 0
        end_col = col_num
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        end_row = row_num
        start_col = int(col_num / 2)
        end_col = start_col + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_bottom_row_sub_chess_board(self, cropped, index):
        ret_pic = self.check_and_draw_shi_line(cropped, index)
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_col = 0
        end_col = col_num
        start_row = int(row_num / 2)
        end_row = start_row + self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_row = 0
        start_col = int(col_num / 2)
        end_col = start_col + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_left_col_sub_chess_board(self, cropped, index):
        ret_pic = cropped
        draw_flag = self.check_is_need_draw_flag(index)
        if draw_flag != None:
            ret_pic = self.draw_center_pao_and_bing_flag(cropped, draw_flag)
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = 0
        end_row = row_num
        end_col = int(col_num / 2)
        start_col = end_col - self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        end_col = col_num
        start_row = int(row_num / 2)
        end_row = start_row + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_right_col_sub_chess_board(self, cropped, index):
        ret_pic = cropped
        draw_flag = self.check_is_need_draw_flag(index)
        if draw_flag != None:
            ret_pic = self.draw_center_pao_and_bing_flag(cropped, draw_flag)
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = 0
        end_row = row_num
        start_col = int(col_num / 2)
        end_col = start_col + self.big_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = 0
        start_row = int(row_num / 2)
        end_row = start_row + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def check_is_need_draw_flag(self, index):
        if index == 19 or index == 25 or index == 64 or index == 70 or\
                index == 29 or index == 31 or index == 33 or index == 56 or index == 58 or index == 60:
            return 'center'
        if index == 27 or index == 54:
            return 'left'
        if index == 35 or index == 62:
            return 'right'
        return None

    def draw_center_sub_chess_board(self, cropped, index):
        row_idx = int(index / 9)
        ret_pic = self.check_and_draw_shi_line(cropped, index)
        draw_flag = self.check_is_need_draw_flag(index)
        if draw_flag != None:
            ret_pic = self.draw_center_pao_and_bing_flag(cropped, draw_flag)
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        start_row = 0
        end_row = row_num
        if row_idx == 4:
            end_row = int(row_num / 2)
        elif row_idx == 5:
            start_row = int(row_num / 2)
        start_col = int(col_num / 2)
        end_col = start_col + self.small_line_size
        ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = 0
        end_col = col_num
        start_row = int(row_num / 2)
        end_row = start_row + self.small_line_size
        return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)

    def draw_center_pao_and_bing_flag(self, cropped, draw_flag):
        self.pao_and_bing_flag_len = 3 * self.small_line_size
        ret_pic = cropped
        space_len = 2 * self.small_line_size
        space_len_bottom_right = 3 * self.small_line_size
        space_len_bottom = 3 * self.small_line_size
        if draw_flag == 'left':
            space_len_bottom_right = space_len
        row_num = cropped.shape[0]
        col_num = cropped.shape[1]
        end_row = int(row_num / 2) - space_len
        start_row = end_row - self.pao_and_bing_flag_len
        start_col = int(col_num / 2) - space_len - self.small_line_size
        end_col = start_col + self.small_line_size
        if draw_flag != 'left':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = int(col_num / 2) + space_len_bottom_right
        end_col = start_col + self.small_line_size
        if draw_flag != 'right':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_row = int(row_num / 2) + space_len_bottom
        end_row = start_row + self.pao_and_bing_flag_len
        start_col = int(col_num / 2) - space_len - self.small_line_size
        end_col = start_col + self.small_line_size
        if draw_flag != 'left':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = int(col_num / 2) + space_len_bottom_right
        end_col = start_col + self.small_line_size
        if draw_flag != 'right':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        end_row = int(row_num / 2) - space_len
        start_row = end_row - self.small_line_size
        end_col = int(col_num / 2) - space_len
        start_col = end_col - self.pao_and_bing_flag_len
        if draw_flag != 'left':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = int(col_num / 2) + space_len_bottom_right
        end_col = start_col + self.pao_and_bing_flag_len
        if draw_flag != 'right':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_row = int(row_num / 2) + space_len_bottom
        end_row = start_row + self.small_line_size
        end_col = int(col_num / 2) - space_len
        start_col = end_col - self.pao_and_bing_flag_len
        if draw_flag != 'left':
            ret_pic = self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        start_col = int(col_num / 2) + space_len_bottom_right
        end_col = start_col + self.pao_and_bing_flag_len
        if draw_flag != 'right':
            return self.draw_line(ret_pic, start_row, end_row, start_col, end_col)
        else:
            return ret_pic

    def check_and_draw_shi_line(self, cropped, index):
        if index == 3 or index == 13 or index == 23 or \
                index == 66 or index == 76 or index == 86:
            start_row = 0
            end_row = cropped.shape[0]
            if index == 3 or index == 66:
                start_row = int(cropped.shape[0] / 2)
            if index == 23 or index == 86:
                end_row = int(cropped.shape[0] / 2)
            if index == 13 or index == 76:
                ret_pic = self.draw_shi_line(cropped, start_row, end_row, 'right_bttom')
                return self.draw_shi_line(ret_pic, start_row, end_row, 'right_top')
            else:
                return self.draw_shi_line(cropped, start_row, end_row, 'right_bttom')
        elif index == 5 or index == 21 or index == 68 or index == 84:
            start_row = 0
            end_row = cropped.shape[0]
            if index == 5 or index == 68:
                start_row = int(cropped.shape[0] / 2)
            if index == 21 or index == 84:
                end_row = int(cropped.shape[0] / 2)
            return self.draw_shi_line(cropped, start_row, end_row, 'right_top')
        return cropped

    def draw_shi_line(self, cropped, start_row, end_row, line_dir):
        ret_pic = cropped
        line_slope = self.per_chessboard_width / self.per_chessboard_height
        row = start_row
        line_size = int(self.small_line_size / 6 * 4)
        if line_dir == 'right_bttom':
            while row < end_row:
                start_col = int(line_slope * row)
                end_col = start_col + line_size
                ret_pic = self.draw_line(ret_pic, row, row + line_size, start_col, end_col)
                row += 1
        else:
            row = end_row
            while row > start_row:
                start_col = cropped.shape[1] - int(line_slope * row)
                end_col = start_col + line_size
                ret_pic = self.draw_line(ret_pic, row, row + line_size, start_col, end_col)
                row -= 1
        return ret_pic

    def draw_line_on_sub_chess_board(self, cropped, index):
        col_idx = index % 9
        if index == 0:
            return self.draw_top_left_sub_chess_board(cropped)
        if index == 8:
            return self.draw_top_right_sub_chess_board(cropped)
        if index == 81:
            return self.draw_bottom_left_sub_chess_board(cropped)
        if index == 89:
            return self.draw_bottom_right_sub_chess_board(cropped)
        if index < 9:
            return self.draw_top_row_sub_chess_board(cropped, index)
        if index >= 81:
            return self.draw_bottom_row_sub_chess_board(cropped, index)
        if col_idx == 0:
            return self.draw_left_col_sub_chess_board(cropped, index)
        if col_idx == 8:
            return self.draw_right_col_sub_chess_board(cropped, index)
        else:
            return self.draw_center_sub_chess_board(cropped, index)

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
            sub_chess_board_label.set_qlabel_index(i)
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
