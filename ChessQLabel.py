# coding=utf-8

from PyQt5.QtWidgets import QLabel
import threading

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
        self.type = None # 'chess_man'/'chess_board'
        self.click_call_back = None
        self.chess_thread = None

    def set_chess_label_info(self, name, type):
        self.name = name
        self.type = type

    def mouseReleaseEvent(self, QMouseEvent):
        if self.click_call_back(self.name) != True:
            return
        if (self.chess_thread == None) or (not self.chess_thread.is_alive()):
            self.chess_thread = WorkerThread(self.chess_board_clicked, 0.35)
            self.chess_thread.start()
        else:
            self.chess_thread.kill_thread()
            self.setVisible(True)

    def chess_lable_connect(self, click_func):
        self.click_call_back = click_func

    def chess_board_clicked(self):
        if self.type != 'chess_man':
            return
        if self.isVisible() == True:
            self.setVisible(False)
        else:
            self.setVisible(True)

