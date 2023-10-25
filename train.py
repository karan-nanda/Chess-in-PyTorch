import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch import optim


class ChessValueDataset(Dataset):
    def __init__(self):
        dat = np.load('/Users/karandeepsinghnanda/Documents/VSCode/Projects/processed/dataset_25M.npz')
        self.X = dat['arr_0']