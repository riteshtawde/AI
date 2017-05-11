'''
@author : Ritesh
@name : Ritesh Tawde
@email : rtawde@iu.edu
'''
import board
import random
import player
import copy

leaf_count = 0

def perft(b, depth):
    global leaf_count      #To avoid UnboundLocalError: local variable 'leaf_count' referenced before assignment
    leaf_count = 0
    return search_depth(b, depth)
    
def search_depth(b, depth):
    global leaf_count
    if depth == 0 or b.last_move_won():
        leaf_count += 1
        #print(leaf_count)
        return
    else:
        list_of_moves = b.generate_moves()
        for move in list_of_moves:
            b.make_move(move)
            search_depth(b, depth - 1)
            b.unmake_last_move()
        return leaf_count
    
def find_win(b, depth):
    p = player.Player()
    p = p.copy_from_board_object(p, b)
    search_for_win(p, b, depth)
    
def search_for_win(p, b, depth):     
    if depth == 0:
        return
    elif b.last_move_won():
        return "NO FORCED WIN IN 8 MOVES"
    else:
        move = p.get_move()
        p.make_move(move)
        p.change_player_turn()
        b.make_move(move)
        search_for_win(p, b, depth - 1)
        p.unmake_last_move()
        b.unmake_last_move()