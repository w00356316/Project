# coding=utf-8

import math

class ChessStrategy():
    def __init__(self):
        self.chess_map = []
        self.update_first_chess_man = {'valid':False, 'action':'None', 'name':'', 'pos':0}
        self.update_second_chess_man = {'valid':False, 'action':'None', 'name':'', 'pos':0}
        self.update_third_chess_man = {'valid':False, 'action':'None', 'name':'', 'pos':0}
        self.update_chess_man_func = None
        self.first_click_info = {'chess_man':None}
        self.second_click_info = {'chess_board_pos':0, 'chess_man':None}
        self.last_click_entry = {'name':'', 'mouse_x': 0, 'mouse_y': 0}
        self.chessboard_width = 0
        self.chessboard_height = 0
        self.per_chessboard_width = 0
        self.per_chessboard_height = 0
        self.chess_man_size = 0
        self.first_left_line = 0
        self.first_top_line = 0
        self.chess_man_strategy_init()
        self.get_chess_board_entry_func = None
        self.black_shuai_init_pos = 0
        self.red_shuai_init_pos = 0

    def set_chess_map(self, chess_map):
        self.chess_map = chess_map

    def set_update_chess_man_func(self, func):
        self.update_chess_man_func = func

    def set_chess_board_entry_func(self, func):
        self.get_chess_board_entry_func = func
        self.set_shuai_init_pos()

    def set_shuai_init_pos(self):
        if self.get_chess_board_entry_func == None:
            print('get_chess_board_entry_func not init error!!!')
            return
        chess_board_entry = self.get_chess_board_entry_func()
        if chess_board_entry == None:
            print('get_chess_board_entry_func error!!!')
            return
        shuai = chess_board_entry.get_pos_info_by_name('red_shuai')
        if shuai == None:
            print('chess_man_red_xiang_rule: [red_shuai] invalid name!!!')
            return
        self.red_shuai_init_pos = shuai['chess_man']['pos']
        shuai = chess_board_entry.get_pos_info_by_name('black_shuai')
        if shuai == None:
            print('chess_man_red_xiang_rule: [black_shuai] invalid name!!!')
            return
        self.black_shuai_init_pos = shuai['chess_man']['pos']

    def chess_size_init(self, chess_man_size, chessboard_width, chessboard_height, per_chessboard_width,
                        per_chessboard_height, first_left_line, first_top_line):
        self.chess_man_size = chess_man_size
        self.chessboard_width = chessboard_width
        self.chessboard_height = chessboard_height
        self.per_chessboard_width = per_chessboard_width
        self.per_chessboard_height = per_chessboard_height
        self.first_left_line = first_left_line
        self.first_top_line = first_top_line

    def chess_man_che_rule(self, change_info):
        if change_info['thread_action'] == 'move':
            return self.che_and_pao_move_rule(change_info)
        if change_info['thread_action'] == 'attack':
            return self.che_and_pao_attack_rule(change_info, 0)
        return True

    def calc_two_pos_row_or_col_distance(self, pos1, pos2, row_or_col):
        if row_or_col == 'row':
            return int(pos1 / 9) - int(pos2 / 9)
        return (pos1 % 9) - (pos2 % 9)

    def chess_man_ma_rule(self, change_info):
        row_dis = self.calc_two_pos_row_or_col_distance(change_info['first_pos'], change_info['second_pos'], 'row')
        col_dis = self.calc_two_pos_row_or_col_distance(change_info['first_pos'], change_info['second_pos'], 'col')
        ma_rule_tab = [[1,2,-9], [-1,2,-9], [1,-2,9], [-1,-2,9], [2,1,-1], [2,-1,-1], [-2,1,1], [-2,-1,1]]
        sub_num = 0
        for ma_rule in ma_rule_tab:
            if (ma_rule[0] == col_dis) and (ma_rule[1] == row_dis):
                sub_num = ma_rule[2]
                break
        if sub_num == 0:
            return False
        sub_num += change_info['first_pos']
        if self.chess_map[sub_num]['chess_man'] != None:
            return False
        return True

    def chess_man_xiang_rule(self, change_info):
        row_dis = self.calc_two_pos_row_or_col_distance(change_info['first_pos'], change_info['second_pos'], 'row')
        col_dis = self.calc_two_pos_row_or_col_distance(change_info['first_pos'], change_info['second_pos'], 'col')
        xiang_rule_tab = [[2, 2, -10], [2, -2, 8], [-2, 2, -8], [-2, -2, 10]]
        sub_num = 0
        for xiang_rule in xiang_rule_tab:
            if (xiang_rule[0] == col_dis) and (xiang_rule[1] == row_dis):
                sub_num = xiang_rule[2]
                break
        if sub_num == 0:
            return False
        sub_num += change_info['first_pos']
        if self.chess_map[sub_num]['chess_man'] != None:
            return False
        return True

    def chess_man_black_xiang_rule(self, change_info):
        if self.chess_man_xiang_rule(change_info) != True:
            return False
        row_dis = self.calc_two_pos_row_or_col_distance(self.black_shuai_init_pos, change_info['second_pos'], 'row')
        if math.fabs(row_dis) > 4:
            return False
        return True

    def chess_man_red_xiang_rule(self, change_info):
        if self.chess_man_xiang_rule(change_info) != True:
            return False
        row_dis = self.calc_two_pos_row_or_col_distance(self.red_shuai_init_pos, change_info['second_pos'], 'row')
        if math.fabs(row_dis) > 4:
            return False
        return True

    def chess_man_black_shi_rule(self, change_info):
        black_shi_rule_tab = {3:[13], 5:[13], 21:[13], 23:[13], 13:[3,5,21,23]}
        if not change_info['first_pos'] in black_shi_rule_tab:
            print('chess_man_black_shi_rule pos({}) err!!!'.format(change_info['first_pos']))
            return False
        rule_arry = black_shi_rule_tab[change_info['first_pos']]
        for pos in rule_arry:
            if pos == change_info['second_pos']:
                return True
        return False

    def chess_man_red_shi_rule(self, change_info):
        red_shi_rule_tab = {84: [76], 86: [76], 66: [76], 68: [76], 76: [84, 86, 66, 68]}
        if not change_info['first_pos'] in red_shi_rule_tab:
            print('chess_man_black_shi_rule pos({}) err!!!'.format(change_info['first_pos']))
            return False
        rule_arry = red_shi_rule_tab[change_info['first_pos']]
        for pos in rule_arry:
            if pos == change_info['second_pos']:
                return True
        return False

    def chess_man_black_shuai_rule(self, change_info):
        return True

    def chess_man_red_shuai_rule(self, change_info):
        return True

    def chess_man_pao_rule(self, change_info):
        if change_info['thread_action'] == 'move':
            return self.che_and_pao_move_rule(change_info)
        if change_info['thread_action'] == 'attack':
            return self.che_and_pao_attack_rule(change_info, 1)
        return True

    def che_and_pao_move_rule(self, change_info):
        start_pos = change_info['first_pos']
        target_pos = change_info['second_pos']
        if self.judge_two_pos_in_same_row(start_pos, target_pos) == True:
            rst = self.judge_exist_pos_num_betwen_two_pos(start_pos, target_pos, 'row')
            if (rst['black'] + rst['red']) > 0:
                return False
            return True
        elif self.judge_two_pos_in_same_col(start_pos, target_pos) == True:
            rst = self.judge_exist_pos_num_betwen_two_pos(start_pos, target_pos, 'col')
            if (rst['black'] + rst['red']) > 0:
                return False
            return True
        else:
            return False

    def che_and_pao_attack_rule(self, change_info, chess_man_num):
        '''
        车或者炮攻击对方时合法性校验
        :param chess_man_num:攻击者和被攻击者之间的棋子个数,规则：炮需要隔一个攻击,车只能攻击与自己相邻的对手
        :return:True:可以攻击,False:不能攻击
        '''
        start_pos = change_info['first_pos']
        target_pos = change_info['second_pos']
        if self.judge_two_pos_in_same_row(start_pos, target_pos) == True:
            rst = self.judge_exist_pos_num_betwen_two_pos(start_pos, target_pos, 'row')
            if (rst['black'] + rst['red']) != chess_man_num:
                return False
            return True
        elif self.judge_two_pos_in_same_col(start_pos, target_pos) == True:
            rst = self.judge_exist_pos_num_betwen_two_pos(start_pos, target_pos, 'col')
            if (rst['black'] + rst['red']) != chess_man_num:
                return False
            return True
        else:
            return False

    def chess_man_black_bing_rule(self, change_info):
        return True

    def chess_man_red_bing_rule(self, change_info):
        return True

    def judge_two_pos_in_same_row(self, pos1, pos2):
        if int(pos1 / 9) == int(pos2 / 9):
            return True
        return False

    def judge_two_pos_in_same_col(self, pos1, pos2):
        if (pos1 % 9) == (pos2 % 9):
            return True
        return False

    def judge_exist_pos_num_betwen_two_pos(self, pos1, pos2, row_or_col):
        '''
        同一行或者列的两个棋子之间存在多少其它棋子,需要保证入参在同一行或者列
        :row_or_col 'row':表示在同一行,'col':表示在同一列
        :return: {'black':num, 'red':num}
        '''
        add = 1
        if row_or_col == 'col':
            add = 9
        min_pos = pos1
        max_pos = pos2
        if min_pos > pos2:
            min_pos = pos2
            max_pos = pos1
        chess_man_num = {'black':0, 'red':0}
        min_pos += add
        while min_pos < max_pos:
            chess_man_handle = self.chess_map[min_pos]['chess_man']
            if chess_man_handle != None:
                chess_man_num[chess_man_handle['color']] += 1
            min_pos += add
        return chess_man_num

    def chess_man_strategy_init(self):
        self.chess_rule_check = {'che':self.chess_man_che_rule,
                                 'ma':self.chess_man_ma_rule,
                                 'black_xiang':self.chess_man_black_xiang_rule,
                                 'red_xiang':self.chess_man_red_xiang_rule,
                                 'black_shi':self.chess_man_black_shi_rule,
                                 'red_shi':self.chess_man_red_shi_rule,
                                 'black_shuai': self.chess_man_black_shuai_rule,
                                 'red_shuai': self.chess_man_red_shuai_rule,
                                 'pao': self.chess_man_pao_rule,
                                 'black_bing': self.chess_man_black_bing_rule,
                                 'red_bing': self.chess_man_red_bing_rule}

    def click_pos_change_process(self):
        result = {}
        result['first_name'] = self.first_click_info['chess_man']['name']
        result['first_pos'] = self.first_click_info['chess_man']['pos']
        result['first_color'] = self.first_click_info['chess_man']['color']
        if self.second_click_info['chess_board_pos'] == 'None':
            result['second_pos'] = self.second_click_info['chess_man']['pos']
            result['second_name'] = self.second_click_info['chess_man']['name']
            result['second_color'] = self.second_click_info['chess_man']['color']
        else:
            result['second_pos'] = self.second_click_info['chess_board_pos']
            result['second_name'] = 'chess_board'
        return result

    def get_chess_type_by_chess_name(self, chess_man_name):
        chess_type_tal = ['che', 'ma', 'black_xiang', 'red_xiang', 'black_shi', 'red_shi', 'black_shuai', 'red_shuai',
                          'pao', 'black_bing', 'red_bing']
        for chess_type in chess_type_tal:
            if chess_type in chess_man_name:
                return chess_type
        print('chess man name({}) invalid!!!\n'.format(chess_man_name))
        return None

    def set_update_chess_man(self, change_info, first_action, second_action, third_action,
                             first_valid, second_valid, third_valid):
        self.update_first_chess_man['valid'] = first_valid
        self.update_second_chess_man['valid'] = second_valid
        self.update_third_chess_man['valid'] = third_valid
        if self.update_first_chess_man['valid'] == True:
            self.update_first_chess_man['action'] = first_action
            self.update_first_chess_man['name'] = change_info['first_name']
            self.update_first_chess_man['pos'] = change_info['first_pos']
        if self.update_second_chess_man['valid'] == True:
            self.update_second_chess_man['action'] = second_action
            self.update_second_chess_man['name'] = change_info['second_name']
            self.update_second_chess_man['pos'] = change_info['second_pos']
        if self.update_third_chess_man['valid'] == True:
            self.update_third_chess_man['action'] = third_action
            self.update_third_chess_man['name'] = change_info['third_name']
            self.update_third_chess_man['pos'] = change_info['third_pos']

    def chess_man_move(self, change_info):
        chess_type = self.get_chess_type_by_chess_name(change_info['first_name'])
        if chess_type == None:
            print('chess_man_move: chess name invalid({})'.format(change_info['first_name']))
            return False
        if change_info['first_pos'] == change_info['second_pos']:
            self.move_chess_man_same_pos()
            return False
        change_info['thread_action'] = 'move'
        if self.chess_rule_check[chess_type](change_info) != True:
            return False
        change_info['second_name'] = change_info['first_name']
        self.set_update_chess_man(change_info, 'Del', 'Add', '', True, True, False)
        return True

    def move_chess_man_same_pos(self):
        label_handle = self.first_click_info['chess_man']['label_handle']
        label_handle.chess_thread.kill_thread()
        label_handle.setVisible(True)

    def attack_rule_check(self, change_info):
        chess_type = self.get_chess_type_by_chess_name(change_info['first_name'])
        if chess_type == None:
            print('attack_rule_check: chess name invalid({})'.format(change_info['first_name']))
            return False
        if change_info['first_pos'] == change_info['second_pos']:
            self.move_chess_man_same_pos()
            return False
        change_info['thread_action'] = 'attack'
        if self.chess_rule_check[chess_type](change_info) != True:
            return False
        change_info['third_name'] = change_info['first_name']
        change_info['third_pos'] = change_info['second_pos']
        self.set_update_chess_man(change_info, 'Del', 'Del', 'Add', True, True, True)
        return True

    def strategy_run(self):
        change_info = self.click_pos_change_process()
        if change_info['second_name'] == 'chess_board':
            if self.chess_man_move(change_info) != True:
                return
        elif self.attack_rule_check(change_info) != True:
            return
        self.update_chess_man_func()
