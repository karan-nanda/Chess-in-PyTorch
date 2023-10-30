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

def explore_leaves(s,v):
    ret = []
    start = time.time()
    v.reset()
    bval = v(s)
    cval, ret = computer_minimax(s,v,0, a = -MAXVAL, b = MAXVAL, big = True)
    eta = time.time() - start
    print("%.2f -> %.2f: explored %d nodes in %.3f seconds %d/sec" % (bval, cval, v.count, eta, int(v.count/eta)))
    return ret

#the board and the engine
s = State()
v = ClassicValuator()

def to_svg(s):
  return base64.b64encode(chess.svg.board(board=s.board).encode('utf-8')).decode('utf-8')

from flask import Flask, Response, request
app = Flask(__name__)

@app.route("/")
def hello():
  ret = open("index.html").read()
  return ret.replace('start', s.board.fen())


def computer_move(s,v):
    move = sorted(explore_leaves(s,v), key=lambda x : x[0],reverse=s.board.turn)
    if len(move) == 0:
        return
    print('top 3 :')
    for i, m in enumerate(move[0:3]):
        print(' ',m)
    print(s.board.turn, 'moving', move[0][1])
    s.board.push(move[0][1])
    
@app.route('/selfplay')
def selfplay():
    s = State()
    
    ret = '<html><head>'
    
    while not s.board.is_game_over():
        computer_move(s,v)
        ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br/>' % to_svg(s)
    print(s.board.result())
    
    return ret



@app.route('/move')
def move():
    if not s.board.is_game_over():
        move = request.args.get('move', default="")
        if move is not None and move != '':
            print('human moves', move)
            

    
        