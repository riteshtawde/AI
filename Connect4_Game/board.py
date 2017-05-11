'''
@author : Ritesh
@name : Ritesh Tawde
@email : rtawde@iu.edu
'''

import copy
import sys
import time

'''References taken :
1) http://inventwithpython.com/extra/fourinarow_text.py
'''
class Board:
    ROWS = 6
    COLUMNS = 7
    MAX_TILES_FOR_WINNING = 4
    EMPTY = '-'
    moveNumber = 0
    Cross = 'X'
    Circle = '0'
    Eval = [0, 1, 2, 3, 4, 5]
    MIN_INFINITY = -99999999
    MAX_INFINITY = 99999999
    GRAPH_DEPTH = 0
    cross_win = False
    circle_win = False
    column = 0
    GLOBAL_PLAYER = 'X'
    MAX_DEPTH = 8
    winnerFound = False
    moveNumber = 1
    
    def __init__(self):
        self.board = [[Board.EMPTY for _ in range(Board.COLUMNS)] for _ in range(Board.ROWS)]
        self.moveNumbers = [[0 for _ in range(Board.COLUMNS)] for _ in range(Board.ROWS)]
        self.firstAvailableRow = [5 for _ in range(Board.COLUMNS)]
        self.move_arr = []
       
    
    def getFirstAvailableRow(self, column):
        return self.firstAvailableRow[column]
            
    def generate_moves(self):
        available_moves = []
        for col in range(Board.COLUMNS):
            if self.firstAvailableRow[col] < 0:
                continue
            else:
                available_moves.append(col)
        return available_moves

    def make_move(self, move):
        if move < 0 or move >= Board.COLUMNS:
            print('invalid move')
            pass
        else:
            self.set(move, Board.GLOBAL_PLAYER)
            self.move_arr.append(move)
        self.change_player_turn()
        # print(str(self))
    
    def unmake_last_move(self):
        col = self.move_arr.pop()
        self.unset(col)
        self.change_player_turn()
    
    def last_move_won(self):
        #self.set_winner()
        if self.set_winner(Board.Cross) or self.set_winner(Board.Circle):    
            return True
        else:
            return False 
        
    def set_winner(self, tile):
         
        for x in range(Board.ROWS - 3):
            for y in range(Board.COLUMNS):
                if self.board[x][y] == tile and self.board[x+1][y] == tile and self.board[x+2][y] == tile and self.board[x+3][y] == tile:
                    return True
        
        for x in range(Board.ROWS):
            for y in range(Board.COLUMNS - 3):
                if self.board[x][y] == tile and self.board[x][y+1] == tile and self.board[x][y+2] == tile and self.board[x][y+3] == tile:
                    return True
         
        for x in range(Board.ROWS - 3):
            for y in range(3, Board.COLUMNS):
                if self.board[x][y] == tile and self.board[x+1][y-1] == tile and self.board[x+2][y-2] == tile and self.board[x+3][y-3] == tile:
                    return True
         
        for x in range(Board.ROWS - 3):
            for y in range(Board.COLUMNS - 3):
                if self.board[x][y] == tile and self.board[x+1][y+1] == tile and self.board[x+2][y+2] == tile and self.board[x+3][y+3] == tile:
                    return True
        return False
        
    def __str__(self):
        # str_ret = '\n'.join([' '.join(str(innerlist) for innerlist in outerlist) for outerlist in Board.board])
        str_ret = ''
        for row in range(Board.ROWS):
            for col in range(Board.COLUMNS):
                str_ret += self.board[row][col]
            str_ret += '\n'
        return str_ret
    
    '''handle exception'''
    def setSign(self, col, mark):
        row = self.firstAvailableRow[col]
        if row < 0:
            print('Column ', col, ' is already full')
        else:    
            # Board.board = self.myDeepCopy(Board.board)
            self.board[row][col] = mark
            self.firstAvailableRow[col] -= 1
        return row
    
    def set(self, col , mark):
        row = self.setSign(col, mark)
        # Board.moveNumbers = self.myDeepCopy(Board.moveNumbers)
        self.moveNumbers[row][col] = self.moveNumber + 1
    
    '''handle exception'''
    def unset(self, col):
        row = self.firstAvailableRow[col]
        if row >= Board.ROWS:
            # print('Column ' + (col + 1) + ' is already empty')
            pass
        else:
            self.firstAvailableRow[col] += 1
            row = self.firstAvailableRow[col];
            # Board.board = self.myDeepCopy(Board.board)
            self.board[row][col] = Board.EMPTY
        
    def getWinningCell(self):
        if Board.winnerFound:
            return self.winningCells
        else:
            return None

    def getMoveNumbers(self):
        return self.moveNumbers
    
    def myDeepCopy(self, list_passed):
        if(isinstance(list_passed, list) or isinstance(list_passed, tuple)):
            return [self.myDeepCopy(element) for element in list_passed]
        else:
            return copy.copy(list_passed)            
    
    def change_player_turn(self):
        if Board.GLOBAL_PLAYER == Board.Circle:
            Board.GLOBAL_PLAYER = Board.Cross
        else:
            Board.GLOBAL_PLAYER = Board.Circle   
    
    def printBoard(self):
        for row in range(Board.ROWS):
            for col in range(Board.COLUMNS):
                sys.stdout.write(self.board[row][col])
            print()
        print('--------')
