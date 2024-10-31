import time
import resource
import sys
import math

class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, dimension: int, config_input: list, goal, cost_function, parent=None, action="Initial", cost=0):
        """
        initialize the board state for the puzzle

        sets up the board based on the given dimension and configuration input,
        checks that the input length matches the expected board size.

        Args:
        - dimension (int): size of one dimension of the board (e.g., for a 3x3 board, dimension = 3)
        - config_input (list): initial configuration of the board as a flat list of tiles
        - goal: target board configuration for solving the puzzle
        - cost_function: function to calculate the cost associated with this board state
        - parent (optional): parent node, used to trace path in search algorithms
        - action (str, optional): description of the action taken to reach this node, default is "Initial"
        - cost (int, optional): initial cost of reaching this state, default is 0

        Raises:
        - AttributeError: if the config_input length doesn't match the board size

        Attributes:
        - board (list): 2D list representation of the board state
        - config (list): stores the flat initial configuration
        - children (list): holds child nodes generated from this node
        - blank_row (int): row index of the blank tile
        - blank_col (int): column index of the blank tile
        - goal: stores the goal configuration
        - cost_function: function for calculating node cost
        """

        if dimension * dimension != len(config_input):
            raise AttributeError("The length of config entered is not correct")

        self.board = [config_input[i:i+3] for i in range(0, dimension * dimension, dimension)]
        self.dimension = dimension
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = 3
        self.config = config_input
        self.children = []
        self.goal = goal
        self.cost_function = cost_function

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.dimension
                self.blank_col = i % self.dimension

    def display(self):
        for i in range(self.dimension):
            print(self.board[i])

    def move_left(self):
        """
        Given the state of the current board, move the one step left.
        This is equivalent to trying to pick the tile that can move left and doing so, if there is one.

        :return: A new PuzzleState instance, that has moved the "left free" tile one step to the left.
        """
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Left",
                               cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Right",
                               cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Up",
                               cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, self.goal, self.cost_function, parent=self, action="Down",
                               cost=self.cost + 1)

    def expand(self, RLDU=True):
        """expand the node"""
        if len(self.children) == 0:
            if RLDU:  #RLDU
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
            else:  #UDLR
                up_child = self.move_up()
                if up_child is not None:
                    self.children.append(up_child)
                down_child = self.move_down()
                if down_child is not None:
                    self.children.append(down_child)
                left_child = self.move_left()
                if left_child is not None:
                    self.children.append(left_child)
                right_child = self.move_right()
                if right_child is not None:
                    self.children.append(right_child)
        return self.children

    def is_solvable(self):
        inversion = 0
        for i in range(len(self.config)):
            for j in range(i + 1, len(self.config)):
                if (self.config[i] > self.config[j]) and self.config[i] != 0 and self.config[j] != 0:
                    inversion += 1
        return inversion % 2 == 0

    def is_goal(self):
        return list(self.config) == self.goal

    def __lt__(self, other):
        return self.cost_function(self) < self.cost_function(other)

    def __le__(self, other):
        return self.cost_function(self) <= self.cost_function(other)
