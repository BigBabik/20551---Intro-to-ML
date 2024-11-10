from Puzzle import PuzzleState
from collections import deque
import heapq
import math

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

    # If the loop ends without finding the goal
    print(f"Goal not found. Number of nodes expanded: {nodes}")

def iddfs(state, max_depth):
    expanded_count = 0
    for depth in range(max_depth):
        print(f"Searching at depth: {depth}")
        final, expanded_count = dls(state, depth, expanded_count)
        if final:
            return True
    print("Goal not found.")
    return False

def dls(state, depth, expanded_count):
    if depth == 0 and state.is_goal(): # why do I check that depth is 0?
                                        # I shouldn't be able to reach a goal in any other depth but stil
        printer("IDDFS", state, expanded_count)
        return True, expanded_count
    if depth > 0:
        for neighbor in state.expand():
            expanded_count += 1
            res, expanded_count = dls(neighbor, depth - 1, expanded_count)
            if res:
                return True, expanded_count
    return False, expanded_count

def compute_gbfs_heuristic(state):
    return sum([abs(item - i) for item, i in enumerate(state.config)])

def gbfs(start_tate, expanded_count=0, calls=0):
    print("Starting GBFS")
    node = start_tate
    frontier = []

    node.cost = compute_gbfs_heuristic(node)
    heapq.heappush(frontier, node)
    reached = set()

    while frontier: # maybe need another term
        calls += 1
        node = heapq.heappop(frontier)
        print(f"[-] Popped is {node.config}")
        if node.is_goal():
            printer("GBFS", node, expanded_count)
            return node, expanded_count

        reached.add(str(node.config))

        for child in node.expand():
            print(f"[-] Child is {child.config}")
            expanded_count += 1
            if str(child.config) not in reached:
                try:
                    child.cost = compute_gbfs_heuristic(child)
                    heapq.heappush(frontier, child)

                    print(f"[*] Pushed {compute_gbfs_heuristic(child)}, {child.config}")
                    reached.add(str(child.config))  # Mark each child as reached
                except:
                    print(f"Crashing on {compute_gbfs_heuristic(child)}, {child.config}")

    # If no solution is found
    print("Goal not found.")
    print(f"Total states expanded: {expanded_count}")
    print(f"Total loop calls: {calls}")
    return None, expanded_count

def manhattan_distance(state):
    total_distance = 0
    size = int(math.sqrt(len(state.config)))  # Assuming square grid
    for index, tile in enumerate(state.config):
        if tile != 0:  # Ignore the empty tile
            target_x, target_y = divmod(tile - 1, size)
            current_x, current_y = divmod(index, size)
            total_distance += abs(current_x - target_x) + abs(current_y - target_y)
    return total_distance


def compute_astar_heuristic(state):
    total_distance = 0

    for index, tile in enumerate(state.config):
        # Calculate the target position of the tile in the goal board
        target_x, target_y = divmod(tile, state.dimension)
        current_x, current_y = divmod(index, state.dimension)

        # Calculate Euclidean distance
        distance = math.sqrt((current_x - target_x) ** 2 + (current_y - target_y) ** 2)
        total_distance += distance

    return total_distance


def a_star(state, expanded=0, calls=0):
    score = 888888  # bigger than any possible value of this heuristic

    if state.is_goal():
        printer("A*", state, expanded)
        return state  # Return the goal state to reconstruct the path if needed

    # Check for maximum expansions or calls after evaluating the goal
    if expanded > 100000 or calls > 500:
        print("Max expanded exceeded or recursion depth")
        return None

    state.expand()  # Expand the current state to generate children
    best_state = None
    best_score = score

    for child in state.children:
        expanded += 1
        score = child.cost + manhattan_distance(child)
        if score < best_score:
            best_state = child
            best_score = score

    # Only recurse if a best state was found
    if best_state is not None:
        print("Recursing to best state {}, {} nodes expanded, score is {}".format(best_state.config, expanded,
                                                                                  best_score))
        return a_star(best_state, expanded, calls + 1)  # Return the result of the recursive call

    return None  # If no best state found, return None
