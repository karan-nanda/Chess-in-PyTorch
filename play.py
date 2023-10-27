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
        vals = torch.load