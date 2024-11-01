from puzzle_state import PuzzleState
from collections import deque


def bfs(start_state):
    nodes = 0
    print("Starting BFS scan.")

    # Initialize the queue with the start state
    queue = deque([start_state])
    visited = set()  # To track visited states and avoid loops
    visited.add(str(start_state.config))

    while queue:
        # Pop the front of the queue
        current_state = queue.popleft()

        # Check if the goal has been reached
        if current_state.is_goal():
            print("Goal reached!")
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