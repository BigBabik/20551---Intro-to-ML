from Puzzle import PuzzleState
from collections import deque
import heapq
import math

def printer(state, nodes):
    print(f"Total of {nodes} states expanded.\nPath to goal:")
    print(state.trace())


def bfs(start_state):
    """
    Implementation of the Breadth First Search algorithm.

    :param start_state: state to start running from.

    :return: The goal stated that was reached
    """
    print("\nBFS")
    expanded_counter = 0

    # Initialize the queue with the start state
    queue = deque([start_state])
    visited = set()  # To track visited states and avoid loops
    visited.add(str(start_state.config))

    while queue:
        # Pop the front of the queue
        current_state = queue.popleft()

        # Check if the goal has been reached
        if current_state.is_goal():
            printer(current_state, expanded_counter)
            return current_state  # Return the goal state to reconstruct the path if needed

        # Generate children and add unvisited ones to the queue

        expanded_counter += 1
        for child in current_state.expand():
            if str(child.config) not in visited:
                visited.add(str(child.config))
                queue.append(child)


    # If the loop ends without finding the goal
    print(f"Goal not found in BFS. Total states expanded: {expanded_counter}.")
    return None

def iddfs(state, max_depth):
    """
    Implementation of the IDDFS algorithm.

    :param state: start state
    :param depth: maximum depth

    :return: True if goal was reached, else False.
    """
    print("\nIDDFS")
    expanded_counter = 0
    for depth in range(max_depth):
        # print(f"Searching at depth: {depth}")
        final, expanded_counter = dfs(state, depth, expanded_counter)
        if final:
            return True
    print(f"Goal not found in IDDFS. Total states expanded: {expanded_counter}.")

    return False

def dfs(state, depth, expanded_counter):
    """
    DFS implementation up to set depth

    :param state: start state
    :param depth: maximum depth
    :param expanded_counter: expanded nodes counter, from previous iterations if needed

    :return: Just a boolean value if the goal was reached. the function already handles printing the path to the goal.
    """
    if state.is_goal():
        printer(state, expanded_counter)
        return True, expanded_counter
    if depth > 0:
        expanded_counter += 1
        for neighbor in state.expand():
            res, expanded_counter = dfs(neighbor, depth - 1, expanded_counter)
            if res:
                return True, expanded_counter
    return False, expanded_counter

def compute_gbfs_heuristic(state):
    """
    Compute the heuristic value for the GBFS search algorithm.

    :param state: state to compute heuristic for

    :return: the overall heuristic measure of the state
    """
    return sum([abs(item - i) for item, i in enumerate(state.config)])

def gbfs(start_state, expanded_counter=0):
    """
    Implementation of the GBFS algorithm.
    Uses a separate heuristic calculation function for easy replacement

    :param start_state: The state to start from
    :param expanded_counter: Optional parameter for setting the expanded nodes counter

    :return: The goal state if found (in it is the path), None if goal state not reached
    """
    print("\nGBFS")
    node = start_state
    frontier = []

    node.cost = compute_gbfs_heuristic(node)
    heapq.heappush(frontier, node)
    reached = set()

    while frontier: # maybe need another term
        node = heapq.heappop(frontier)
        if node.is_goal():
            printer(node, expanded_counter)
            return node, expanded_counter

        reached.add(str(node.config))

        expanded_counter += 1
        for child in node.expand():
            if str(child.config) not in reached:
                child.cost = compute_gbfs_heuristic(child)
                heapq.heappush(frontier, child)

                reached.add(str(child.config))  # Mark each child as reached


    # If no solution is found
    print(f"Goal not found in GBFS. Total states expanded: {expanded_counter}.")
    return None, expanded_counter

def manhattan_distance(state):
    total_distance = 0
    size = state.dimension
    for index, tile in enumerate(state.config):
        if tile != 0:  # Ignore the empty tile
            target_x, target_y = divmod(tile - 1, size)
            current_x, current_y = divmod(index, size)
            total_distance += abs(current_x - target_x) + abs(current_y - target_y)
    return total_distance

def compute_astar_heuristic(state, distance_to):
    """
    Compute the heuristic value for the A* search algorithm.

    :param state: state to compute heuristic for
    :param distance_to: the distance to the state

    :return: the overall heuristic measure of the state
    """
    #return distance_to + manhattan_distance(state)
    total_distance = 0

    for index, tile in enumerate(state.config):
        # Calculate the target position of the tile in the goal board
        target_x, target_y = divmod(tile, state.dimension)
        current_x, current_y = divmod(index, state.dimension)

        # Calculate Euclidean distance
        distance = math.sqrt((current_x - target_x) ** 2 + (current_y - target_y) ** 2)
        total_distance += distance

    return distance_to + total_distance

def a_star(start_state, expanded_counter=0):
    """
    Implementation of the A* algorithm
    Uses a separate heuristic calculation function for easy replacement

    :param start_state: The state to start from
    :param expanded_counter: Optional parameter for setting the expanded nodes counter

    :return: The goal state if found (in it is the path), None if goal state not reached
    """
    print("\nA*")
    node = start_state
    frontier = []
    actual = 0

    node.cost = compute_astar_heuristic(node, actual)
    heapq.heappush(frontier, node)
    reached = set()

    while frontier: # maybe need another term
        node = heapq.heappop(frontier)
        if node.is_goal():
            printer(node, expanded_counter)
            return node, expanded_counter
        else:
            actual += 1 # definitely needs to take another action so g(n) gets increased

        reached.add(str(node.config))

        expanded_counter += 1
        for child in node.expand():
            if str(child.config) not in reached:
                child.cost = compute_astar_heuristic(node, actual)
                heapq.heappush(frontier, child)

                reached.add(str(child.config))  # Mark each child as reached

    # If no solution is found
    print(f"Goal not found in A*. Total states expanded: {expanded_counter}.")
    return None, expanded_counter

