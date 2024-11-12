# Define moves as row, col offsets for each action
LEGAL_MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}


class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, dimension: int, config_input: list, goal: list, parent=None, action="Initial", cost=0):
        """
        Initializes the board state for the puzzle.

        Sets up the initial configuration of the board based on the provided dimension and
        configuration input, checks input length, and initializes attributes like the board's
        dimension, parent, action, cost, and goal state.

        :param dimension: The dimension of the board (e.g., 3 for a 3x3 board).
        :param config_input: A list representing the initial configuration of the puzzle board.
                             The list length must match the square of the board's dimension.
        :param goal: A list representing the goal configuration for the puzzle.
        :param parent: The parent node in the puzzle's search tree, used for backtracking.
                       Defaults to None for the root node.
        :param action: The action taken to reach this state from the parent state. Defaults to "Initial" and is .
                       populated during calls to self.expand() for the children nodes.
        :param cost: The cost to reach this state. Defaults to 0.

        Attributes initialized:
        - board: 2D list representation of the board state, used primarily for display purposes.
        - dimension: The board's dimension, which determines the board size.
        - cost: The cost associated with reaching this state from the root state.
        - parent: The parent node, allowing backtracking to the previous board state for solution retrieval.
        - action: Describes the move that led to this board state from the parent (e.g., "up", "down").
        - config: The flat list representation of the board, used to determine tile positions.
        - children: A list to store child nodes generated from this board state.
        - goal: The target configuration for the puzzle. In our case will usually be [0,1,2,3,4,5,6,7,8]
        - movement: a movement map for calculating target indices. Is based on the dimension parameter.
        - blank_row and blank_col: The current row and column positions of the blank tile (0).

        Example:
            For a 3x3 puzzle, an example configuration input might be:
            config_input = [1, 2, 3, 4, 5, 6, 7, 8, 0] representing:
            1 2 3
            4 5 6
            7 8 0
        """

        if dimension * dimension != len(config_input):
            raise AttributeError("The length of config entered is not correct")

        self.board = [config_input[i:i+3] for i in range(0, dimension * dimension, dimension)] # for printing
        self.dimension = dimension
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config_input
        self.children = []
        self.goal = goal    # what is the goal state of this game. Will always be the same in our case but was used for testing.
        self.movement = {'Up': self.dimension, 'Down': -self.dimension, 'Left': 1, 'Right': -1}

        for i, item in enumerate(self.config):  # calculate the row and col the blank is in, easier down the road
            if item == 0:
                self.blank_row = i // self.dimension
                self.blank_col = i % self.dimension


    def display(self):
        """
        Helper function for printing states

        :return: None
        """
        for i in range(self.dimension):  # print the i'th row every time
            print(self.board[i])

    def move(self, direction):
        blank_index = self.blank_row * self.dimension + self.blank_col
        target = blank_index + self.movement[direction]

        new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(self.dimension, new_config, self.goal, parent=self, action=direction,
                           cost=self.cost + 1)

    def move_left(self):
        """
        Given the state of the current board, move the one step left.
        This is equivalent to trying to pick the only tile that can move left and doing so, if there is one.

        :return: A new PuzzleState instance, that has moved the "left free" tile one step to the left.
        """
        if self.blank_col == self.dimension - 1:
            return None
        else:
            return self.move("Left")

    def move_right(self):
        if self.blank_col == 0:
            return None
        else:
            return self.move("Right")

    def move_up(self):
        if self.blank_row == self.dimension - 1:
            return None
        else:
            return self.move("Up")

    def move_down(self):
        if self.blank_row == 0:
            return None
        else:
            return self.move("Down")

    def expand(self, RLDU=True):
        """
        Expands the current node by generating its children nodes based on possible moves.

        If the node has no children, this method generates child nodes by applying movement functions
        in the order specified by the RLDU flag. Each movement function (e.g., move_right, move_left)
        returns a child node if the move is valid, otherwise, it returns None. Only valid moves that
        generate non-None child nodes are added to the children list.

        :param RLDU: If True, moves are generated in Right, Left, Down, Up order (RLDU).
                     If False, moves are generated in Up, Down, Left, Right order (UDLR).
                     This ordering can be useful for customizing the traversal behavior and affects results.

        :return: A list of child nodes created by applying each valid move to the current node.
        """
        if len(self.children) == 0:
            if RLDU:  #RLDU
                for move in [self.move_right, self.move_left, self.move_down, self.move_up]:
                    child = move()
                    if child is not None:
                        self.children.append(child)
            else:  #UDLR
                for move in [self.move_up, self.move_down, self.move_left, self.move_right]:
                    child = move()
                    if child is not None:
                        self.children.append(child)
        return self.children

    @staticmethod
    def find_moved_tile(current_state):

        # Find the position of the blank tile
        blank_index = current_state.config.index(0)

        # Get the row, col offset for the given action
        if current_state.action not in LEGAL_MOVES:
            raise ValueError("Invalid action.")

        row_offset, col_offset = LEGAL_MOVES[current_state.action]
        target = blank_index + row_offset * current_state.dimension + col_offset

        if 0 <= target < len(current_state.config):
            return current_state.config[target]  # Return the tile that was moved
        else:
            return None  # Invalid move

    def trace(self):
        """
        The function returns all tiles moved up to this state.
        It can be done deterministically because each state has the attribute action that indicates what was
        done to reach it, and only 1 or less tiles in each state can legally perform any given action.

        :return: list of numbers, each number is a tile
        """
        ancestors = []
        node = self
        while node is not None and node.action != "Initial":
            ancestors.append(PuzzleState.find_moved_tile(node))
            node = node.parent  # Move up to the parent node
        ancestors.reverse()
        return ancestors

    def is_goal(self):
        """
        Checks if the current state is a goal state.
        :return:
        """
        return list(self.config) == self.goal

    def __lt__(self, other):
        """
        Implement less than operator for use of priority que in algoritm implementations.

        :param other: The other state
        :return: bool. if lesser than
        """
        return self.cost < other.cost