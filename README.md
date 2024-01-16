# Chess-in-PyTorch

This repository contains a comprehensive chess engine implemented in Python. The engine combines traditional board evaluation methods with a neural network for move generation and position evaluation. The engine also features a web interface for interactive gameplay.

## Table of Contents
- [Introduction](#introduction)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Self-play](#self-play)
  - [Interactive Mode](#interactive-mode)
- [Chess Engine](#chess-engine)
  - [Minimax Algorithm](#minimax-algorithm)
  - [Neural Network Model](#neural-network-model)
  - [State Representation](#state-representation)
- [Dataset](#dataset)
- [Training the Model](#training-the-model)
- [Web Interface](#web-interface)
- [Acknowledgments](#acknowledgments)

## Introduction
This chess engine provides a robust implementation of a chess-playing AI that utilizes a combination of traditional board evaluation methods and a neural network. The engine supports self-play, allowing it to play against itself, and an interactive mode where users can play against the AI through a web interface.

## Dependencies
Make sure you have the following dependencies installed before running the engine:

- Python 3.x
- Flask
- PyTorch
- Numpy
- python-chess

Install the dependencies using:
```bash
pip install flask torch numpy python-chess
```

## Usage
### Self-play
To see the engine play against itself, run the following command:
```bash
python chess_engine.py selfplay
```

### Interactive Mode
To play against the chess engine, run the following command:
```bash
python chess_engine.py
```
This will start a web server, and you can access the chess board through your web browser.

## Chess Engine
The chess engine is a combination of traditional board evaluation methods and a neural network for move generation and position evaluation. It includes classes and functions for the minimax algorithm, neural network model, and state representation.

### Minimax Algorithm
The minimax algorithm with alpha-beta pruning is implemented in the `computer_minimax` function in `chess_engine.py`. It explores possible moves and evaluates the best move using the provided board valuation function.

### Neural Network Model
The neural network model is defined in the `Net` class in `train.py`. It uses a convolutional neural network (CNN) architecture to evaluate board positions and is trained on a custom chess dataset.

### State Representation
The `State` class in `state.py` provides methods for representing the state of the chess board. It includes key generation, serialization of the board state into a binary format, and obtaining legal moves for the current board position.

## Dataset
The dataset used for training the neural network is loaded from a preprocessed file (`dataset_25M.npz`). It includes board positions and corresponding target values for training.

## Training the Model
If you want to train the neural network model yourself, follow these steps:

1. Make sure you have the required dependencies installed.
2. Run the training script:
    ```bash
    python train.py
    ```
3. The trained model will be saved in the `nets/value.pth` file.

## Web Interface
The engine includes a simple web interface using Flask, allowing you to play against the AI in your browser. Access the interface at your localhost address after starting the engine.

## Acknowledgments
This code is inspired by various chess engines and AI implementations available in the open-source community. Special thanks to the creators and contributors of the [python-chess](https://python-chess.readthedocs.io/) library for providing a powerful and user-friendly interface for chess programming in Python.
