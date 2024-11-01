from puzzle_state import PuzzleState
from collections import deque


def printer(algo, state, nodes):
    print(f"\n{algo}\nTotal of {nodes} states expanded.\nPath to goal:")
    print(state.trace())


def bfs(start_state):
    nodes = 0

    # Initialize the queue with the start state
    queue = deque([start_state])
    visited = set()  # To track visited states and avoid loops
    visited.add(str(start_state.config))

    while queue:
        # Pop the front of the queue
        current_state = queue.popleft()
        nodes += 1

        # Check if the goal has been reached
        if current_state.is_goal():
            printer("BFS", current_state, nodes)
            return current_state  # Return the goal state to reconstruct the path if needed

        # Generate children and add unvisited ones to the queue
        for child in current_state.expand():
            if str(child.config) not in visited:
                visited.add(str(child.config))
                queue.append(child)
                #child.parent = current_state  # Keep track of the path

    # If the loop ends without finding the goal
    print("Goal not found.")
    print(f"Number of nodes expanded: {nodes}")

def dfs(state):
    pass