# coding=utf-8

class ChessCompetition():
    def __init__(self):
        self.cur_player = 'red' # 'red','black'
        self.winner = '' # 'red','black'

    def change_cur_player(self):
        if self.cur_player == 'red':
            self.cur_player = 'black'
        else:
            self.cur_player = 'red'

    def set_winner(self, winner):
        self.winner = winner
