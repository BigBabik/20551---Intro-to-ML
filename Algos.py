from Puzzle import PuzzleState
from collections import deque
import heapq
import math

def printer(state, nodes):
    print(f"Total of {nodes} states expanded.\nPath to goal:")
    print(state.trace())


def bfs(start_state):
    print("\nBFS")
    nodes = 0

    # Initialize the queue with the start state
    queue = deque([start_state])
    visited = set()  # To track visited states and avoid loops
    visited.add(str(start_state.config))

    while queue:
        # Pop the front of the queue
        current_state = queue.popleft()

        # Check if the goal has been reached
        if current_state.is_goal():
            printer(current_state, nodes)
            return current_state  # Return the goal state to reconstruct the path if needed

        # Generate children and add unvisited ones to the queue
        for child in current_state.expand():
            if str(child.config) not in visited:
                visited.add(str(child.config))
                queue.append(child)
        nodes += 1

    # If the loop ends without finding the goal
    print(f"Goal not found in IDDFS. Total states expanded: {nodes}.")

def iddfs(state, max_depth):
    print("\nIDDFS")
    expanded_count = 0
    for depth in range(max_depth):
        # print(f"Searching at depth: {depth}")
        final, expanded_count = dfs(state, depth, expanded_count)
        if final:
            return True
    print(f"Goal not found in IDDFS. Total states expanded: {expanded_count}.")

    return False

def dfs(state, depth, expanded_count):
    if depth == 0 and state.is_goal(): # why do I check that depth is 0?
                                        # I shouldn't be able to reach a goal in any other depth but stil
        printer(state, expanded_count)
        return True, expanded_count
    if depth > 0:
        for neighbor in state.expand(RLDU=False):
            res, expanded_count = dfs(neighbor, depth - 1, expanded_count)
            expanded_count += 1
            if res:
                return True, expanded_count
    return False, expanded_count

def compute_gbfs_heuristic(state):
    return sum([abs(item - i) for item, i in enumerate(state.config)])

def gbfs(start_state, expanded_count=0, calls=0):
    print("\nGBFS")
    node = start_state
    frontier = []

    node.cost = compute_gbfs_heuristic(node)
    heapq.heappush(frontier, node)
    reached = set()

    while frontier: # maybe need another term
        calls += 1
        node = heapq.heappop(frontier)
        if node.is_goal():
            printer(node, expanded_count)
            return node, expanded_count

        reached.add(str(node.config))

        for child in node.expand():
            expanded_count += 1
            if str(child.config) not in reached:
                child.cost = compute_gbfs_heuristic(child)
                heapq.heappush(frontier, child)

                reached.add(str(child.config))  # Mark each child as reached


    # If no solution is found
    print(f"Goal not found in GBFS. Total states expanded: {expanded_count}. Total loop calls: {calls}")
    return None, expanded_count

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

def a_star(start_state, expanded_count=0, calls=0):
    print("\nA*")
    node = start_state
    frontier = []
    actual = 0

    node.cost = compute_astar_heuristic(node, actual)
    heapq.heappush(frontier, node)
    reached = set()

    while frontier: # maybe need another term
        calls += 1
        node = heapq.heappop(frontier)
        if node.is_goal():
            printer(node, expanded_count)
            return node, expanded_count
        else:
            actual += 1 # definitely needs to take another action so g(n) gets increased

        reached.add(str(node.config))

        for child in node.expand():
            expanded_count += 1
            if str(child.config) not in reached:
                child.cost = compute_astar_heuristic(node, actual)
                heapq.heappush(frontier, child)

                reached.add(str(child.config))  # Mark each child as reached

    # If no solution is found
    print(f"Goal not found in A*. Total states expanded: {expanded_count}. Total loop calls: {calls}")
    return None, expanded_count

