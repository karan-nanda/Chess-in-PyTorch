from __future__ import print_function
import os
import chess
import time
import chess.svg
import traceback
import base64
from state import State

class Valuator(object):
    def __init__(self):
        import torch
        from train import Net
        vals = torch.load("nets/value.pth", map_location=lambda storage, loc: storage)
        self.model = Net()
        self.model.load_state_dict(vals)
        
        def __call__(self,s):
            brd = s.serialize()[None]
            output = self.model(torch.tensor(brd).float())
            return float(output.data[0][0])
        
MAXVAL = 10000
class ClassicValuator(object):
    values = {chess.PAWN: 1,
                chess.KNIGHT : 3,
                chess.BISHOP : 3,
                chess.ROOK : 5,
                chess.QUEEN : 9,
                chess.KING : 0
                }
        
    def __init__(self):
        self.reset()
        self.memo = {}
            
            
    def reset(self):
        self.count = 0
            
    def __call__(self,s):
        self.count += 1
        key = s.key()
        if key not in self.memo:
            self.memo[key] = self.value(s)
        return self.memo[key]
        
    def value(self,s):
        b = s.board
            
        if b.is_game_over():
            if b.result() == '1-0':
                return MAXVAL
            elif b.result() == '0-1':
                return -MAXVAL
            else:
                return 0
            
        val = 0.0
        
        pm = s.board.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                val += tval
            else:
                val -= tval
                
        bak = b.turn
        b.turn = chess.WHITE
        val += 0.1 * b.legal_moves.count()
        b.turn = chess.BLACK
        val -= 0.1 * b.legal_moves.count()
        b.turn = bak
        
        
        return val

def computer_minimax(s,v, depth, a,b, big = False):
    if depth >= 5 or s.board.is_game_over():
        return v(s)
    
    #White becomes the maximizing player
    turn = s.board.turn
    if turn == chess.WHITE:
        ret = -MAXVAL
    else:
        ret = MAXVAL
    if big:
        bret = []
        
        
    isort = []
    for e in s.board.legal_moves:
        s.board.push(e)
        isort.append((v(s),e))
        s.board.pop()
    move = sorted (isort, key = lambda x : x[0], reverse=s.board.turn)
    
    #Beam search beyond depth of 3
    if depth >= 3:
        move = move[:10]
    
    for e in [x[1] for x in move]:
        s.board.push(e)
        tval = computer_minimax(s,v,depth +1,a,b)
        s.board.pop()
        if big:
            bret.append((tval, e))
        if turn == chess.WHITE:
            ret = max(ret,tval)
            a = max(a, ret)
            if a >= b:
                break
        
        else:
            ret = min(ret, tval)
            b  = min(b,ret)
            if a >= b:
                break
    if big:
        return ret,bret
    else:
        return ret


        