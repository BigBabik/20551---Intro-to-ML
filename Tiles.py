from Puzzle import PuzzleState
import Algos
import random

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


def run_algos(config: list):
    state = PuzzleState(dimension=DIMENSION, config_input=config, goal=list(range(9)), cost_function=None)
    state.display()

    b = Algos.bfs(state)
    if b is None:
        return None
    #Algos.iddfs(state, 15)
    Algos.gbfs(state)
    #Algos.a_star(state)

def main():
    #config = get_user_input()
    run_algos([1,4,0,5,8,2,3,6,7])

    for i in range(10):
        print("\n\n\n")
        config = list(range(9))  # Create a list from 0 to 8
        random.shuffle(config)  # Shuffle the list
        #run_algos(config)


if __name__ == '__main__':
    main()
