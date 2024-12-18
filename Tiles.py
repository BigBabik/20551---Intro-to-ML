from Puzzle import PuzzleState
import Algos
import random

DIMENSION = 3

def get_user_input():
    """
    prompts user to input the 8-tile game configuration,
    where each number (0-8) is separated by a single space

    :returns: list of integers representing the board configuration
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
    state = PuzzleState(dimension=DIMENSION, config_input=config, goal=list(range(9)))
    state.display()

    b = Algos.bfs(state)
    if b is None:
        print("Skipping config because goal not reached in BFS")
        return None
    Algos.iddfs(state, 11)
    Algos.gbfs(state)
    Algos.a_star(state)

def run_tests():
    run_algos([1, 4, 0, 5, 8, 2, 3, 6, 7])

    for i in range(5):
        config = list(range(9))  # Create a list from 0 to 8
        random.shuffle(config)  # Shuffle the list
        print("\n\n\n")
        run_algos(config)

def main():
    config = get_user_input()
    run_algos(config)
    #run_tests()

if __name__ == '__main__':
    main()
