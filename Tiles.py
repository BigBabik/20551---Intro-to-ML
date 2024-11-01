from distutils.command.config import config

import puzzle_state
from puzzle_state import PuzzleState


DIMENSION = 3


def get_user_input():
    """
    prompts user to input the 8-tile game configuration,
    where each number (0-8) is separated by a single space

    Returns:
    - list of integers representing the board configuration

    Raises:
    - ValueError if input doesn't contain exactly 9 numbers from 0 to 8
    """
    while True:
        try:
            config_input = input("Enter the 8-tile game configuration (0-8, separated by spaces): ")
            config = list(map(int, config_input.split()))

            if len(config) != 9 or sorted(config) != list(range(9)):
                raise ValueError("Input must contain numbers 0-8 exactly once.")

            return config
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def main():
    #config = get_user_input()
    config = [1, 4, 2, 3, 0, 5, 6, 7, 8]

    state = PuzzleState(dimension=DIMENSION, config_input=config, goal=list(range(9)), cost_function=None)
    state.display()

    # test movement
    left = state.move_left()
    right = state.move_right()
    up = state.move_up()
    down = state.move_down()

    print("\nDisplaying left:")
    left.display()

    print("\nDisplaying right:")
    right.display()

    print("\nDisplaying down:")
    down.display()

    print("\nDisplaying up:")
    up.display()



if __name__ == '__main__':
    main()
