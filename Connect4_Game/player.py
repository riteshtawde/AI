'''
@author : Ritesh
@name : Ritesh Tawde
@email : rtawde@iu.edu
'''
from board import Board


'''References taken :
1) http://www.brian-borowski.com/software/connectfour/
'''
class Player:
    board = Board()
    moveNumber = 0
    movesSuggested = []
    GLOBAL_PLAYER = 'X'
    
    def __init__(self):
        self.local_board = [[Board.EMPTY for _ in range(Board.COLUMNS)] for _ in range(Board.ROWS)]
        self.moveNumbers = [[0 for _ in range(Board.COLUMNS)] for _ in range(Board.ROWS)]
        self.firstAvailableRow = [5 for _ in range(Board.COLUMNS)]
        self.move_arr = []
    
    def name(self):
        return 'Nish'
    
    def make_move(self, move):
        if move < 0 or move >= Board.COLUMNS:
            print('invalid move')
        else:
            self.set(move, Board.GLOBAL_PLAYER)
        self.move_arr.append(move)
    
    def setSign(self, col, mark):
        row = self.firstAvailableRow[col]
        if row < 0:
            #print('Column ', col, ' is already full')
            pass
        else:    
            #Player.local_board = Player.board.myDeepCopy(Player.local_board)
            self.local_board[row][col] = mark
            self.firstAvailableRow[col] -= 1
        return row
    
    def set(self, col , mark):
        row = self.setSign(col, mark)
        #Player.moveNumbers = Player.board.myDeepCopy(Player.moveNumbers)
        self.moveNumbers[row][col] = Player.moveNumber + 1
        
    def unset(self, col):
        row = self.firstAvailableRow[col]
        if row >= Board.ROWS-1:
            #print('Column ' , (col + 1) , ' is already empty')
            pass
        else:
            self.firstAvailableRow[col] += 1
            row = self.firstAvailableRow[col];
            #Player.local_board = Player.board.myDeepCopy(Player.local_board)
            self.local_board[row][col] = Board.EMPTY
    
    def unmake_last_move(self):
        col = self.move_arr.pop()
        self.unset(col)
        self.change_player_turn()  
    
    def change_player_turn(self):
        if Board.GLOBAL_PLAYER == Board.Circle:
            Board.GLOBAL_PLAYER = Board.Cross
        else:
            Board.GLOBAL_PLAYER = Board.Circle  
        
    def isEmpty(self):
        for row in range(Board.ROWS):
            for col in range(Board.COLUMNS):
                if Board.EMPTY != self.local_board[row][col]:
                    return False
        return True
        
    def get_move(self):
        move = self.alpha_beta_pruning(Board.GLOBAL_PLAYER)
        #print('move suggested by my player : ', move)
        #Player.movesSuggested.append(move)
        return move
    
    def isEmptyColumn(self, column):
        return self.firstAvailableRow[column] != -1
    
    def getScoreIncVal(self, cross, circle, player):
        if cross == circle:
            if(player == Board.Cross):
                return -1
            return 1
        elif cross < circle:
            if player == Board.Cross:
                return Board.Eval[circle] - Board.Eval[cross]
            return Board.Eval[circle + 1] - Board.Eval[cross]
        else:
            if player == Board.Cross:
                return -Board.Eval[cross + 1] + Board.Eval[circle]
            return -Board.Eval[cross] + Board.Eval[circle]    
    
        
    def heuristic(self, player, col, depth, maxDepth):
        total_score = 0
        row = self.firstAvailableRow[col] + 1
        row_of_board = self.local_board[row]
        a = col - 3
        start_column = a if a >= 0 else 0
        end_column = Board.COLUMNS - 3 - (start_column - a)
        cntCross = 0
        cntCircle = 0
        
        '''row heuristic'''
        for i in range(start_column, end_column):
            cntCross = 0
            cntCircle = 0
            for b in range(4):
                sign = row_of_board[i + b]
                if sign == Board.Cross:
                    cntCross += 1
                elif sign == Board.Circle:
                    cntCircle += 1
            if cntCross == 4:
                Board.cross_win = True
                if depth <= 2:
                    return Board.MIN_INFINITY + 1
            elif cntCircle == 4:
                Board.circle_win = True
                if depth <= 2:
                    return Board.MAX_INFINITY - 1
            total_score += self.getScoreIncVal(cntCross, cntCircle, player) 
        
        '''column heuristic'''
        end_row = min(Board.ROWS, row + 4)
        cntCross = 0
        cntCircle = 0
        for i in range(row, end_row):
            sign = self.local_board[i][col]
            if sign == Board.Cross:
                cntCross += 1
            elif sign == Board.Circle:
                cntCircle += 1
        if cntCross == 4:
            Board.cross_win = True
            if depth <= 2:
                return Board.MIN_INFINITY + 1
            elif cntCircle == 4:
                Board.circle_win = True
                if depth <= 2:
                    return Board.MAX_INFINITY - 1
        total_score += self.getScoreIncVal(cntCross, cntCircle, player)
       
        '''right to left diagonal heuristic'''
        minval = min(row, col)
        start_row = row - minval
        start_column = col - minval
        for i, j in zip(range(start_row, Board.ROWS - 3), range(start_column, Board.COLUMNS - 3)):
            cntCross = 0
            cntCircle = 0
            for k in range(4):
                sign = self.local_board[i + k][j + k]
                if sign == Board.Cross:
                    cntCross += 1
                elif sign == Board.Circle:
                    cntCircle += 1
            if cntCross == 4:
                Board.cross_win = True
                if depth <= 2:
                    return Board.MIN_INFINITY + 1
            elif cntCircle == 4:
                Board.circle_win = True
                if depth <= 2:
                    return Board.MAX_INFINITY - 1
            total_score += self.getScoreIncVal(cntCross, cntCircle, player)
    
        '''left to right diagonal heuristic'''
        minval = min(Board.ROWS - 1 - row, col)
        start_row = row + minval
        start_column = col - minval
        for i, j in zip(range(start_row, 2, -1), range(start_column, Board.COLUMNS - 3)):
            cntCircle = 0
            cntCross = 0
            for k in range(4):
                sign = self.local_board[i - k][j + k]
                if sign == Board.Cross:
                    cntCross += 1
                elif sign == Board.Circle:
                    cntCircle += 1
            if cntCross == 4:
                Board.cross_win = True
                if depth <= 2:
                    return Board.MIN_INFINITY + 1
            elif cntCircle == 4:
                Board.circle_win = True
                if depth <= 2:
                    return Board.MAX_INFINITY - 1
            total_score += self.getScoreIncVal(cntCross, cntCircle, player)
        return total_score
    
    def utility_func_circle(self, alpha, beta, col, depth, maxDepth):
        Board.GRAPH_DEPTH += 1
        prune_val = Board.MIN_INFINITY
        score = 0
        if col != -1:
            score = self.heuristic(Board.Cross, col, depth, maxDepth)
            if Board.cross_win:
                return score
        
        if depth == maxDepth:
            return score    
        for i in range(Board.COLUMNS):
            if self.isEmptyColumn(i):
                self.setSign(i, Board.Circle)
                eval_score = self.utility_func_cross(alpha, beta, i, depth + 1, maxDepth)
                self.unset(i)
                if eval_score > prune_val:
                    prune_val = eval_score
                    if depth == 0:
                        Board.column = i
                if eval_score > alpha:
                    alpha = eval_score
                if alpha >= beta:
                    return alpha        
        if prune_val == Board.MIN_INFINITY:
            return 0           
        return prune_val
                
    def utility_func_cross(self, alpha, beta, col, depth, maxDepth):
        Board.GRAPH_DEPTH += 1
        prune_val = Board.MAX_INFINITY
        score = 0
        if col != -1:
            score = self.heuristic(Board.Circle, col, depth, maxDepth)
            if Board.circle_win:
                return score
        
        if depth == maxDepth:
            return score
        
        for i in range(Board.COLUMNS):
            if self.isEmptyColumn(i):
                self.setSign(i, Board.Cross)
                eval_score = self.utility_func_circle(alpha, beta, i, depth + 1, maxDepth)
                self.unset(i)
                if eval_score > prune_val:
                    prune_val = eval_score
                    if depth == 0:
                        Board.column = i
                    if eval_score < beta:
                        beta = eval_score
                    if alpha >= beta:
                        return beta
            if prune_val == Board.MAX_INFINITY:
                return 0
            return prune_val
                    
    def alpha_beta_pruning(self, player):
        Board.cross_win = False
        Board.circle_win = False
        if player == Board.Circle:
            self.utility_func_circle(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, 1)
            if Board.circle_win:
                return Board.column
            Board.cross_win = False
            Board.circle_win = False
            self.utility_func_cross(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, 1)
            if Board.cross_win:
                return Board.column
            self.utility_func_circle(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, Board.MAX_DEPTH)
        else:
            self.utility_func_cross(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, 1)
            if Board.cross_win:
                return Board.column
            Board.cross_win = False
            Board.circle_win = False
            self.utility_func_circle(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, 1)
            if Board.circle_win:
                return Board.column
            self.utility_func_cross(Board.MIN_INFINITY + 1, Board.MAX_INFINITY - 1, -1, 0, Board.MAX_DEPTH)
        return Board.column
    
    def copy_from_board_object(self, player, board):
        self.local_board = board.board
        self.moveNumbers = board.moveNumbers
        self.firstAvailableRow = board.firstAvailableRow
        return player