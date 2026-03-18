import heapq

def heuristic(state, goal):  # Manhattan distance:- distance between current state and goal state disctance of each tile from its goal position
    distance = 0
    for i in range(9):
        if state[i] != 0:                                   #skipping blank tile as we have considered 0 as blank tile . 
            goal_index = goal.index(state[i])      #using index function to find the position of that particular tile in goal matrix . ( state[i] represents the i th index of matrix state ) . 
            r1 = i // 3
            c1 = i % 3
            r2 = goal_index // 3                    #calculating row and column of current state and goal state using integer division and modulus operator . 
            c2 = goal_index % 3
            distance += abs(r1 - r2) + abs(c1 - c2)
    return distance

def get_neighbors(state):
    neighbors = []
    blank = state.index(0)
    moves = [-3, 3, -1, 1]   #-3 and + 3 because going one row up and down requires a change of 3 in the index . -1 and +1 because going left and right requires a change of 1 in the index . 

    for move in moves:
        new_pos = blank + move

        if new_pos < 0 or new_pos > 8:     #checking if the new position is out of bounds (less than 0 or greater than 8) .
            continue
        if move == -1 and blank % 3 == 0: #checking if the move is left and the blank tile is in the leftmost column (index 0, 3, 6) . If so, we cannot move left because it would wrap around to the rightmost column . 
            continue
        if move == 1 and blank % 3 == 2:  #checking if the move is right and the blank tile is in the rightmost column (index 2, 5, 8) . If so, we cannot move right because it would wrap around to the leftmost column . 
            continue

        new_state = list(state)                                                         #creating a new state by swapping the blank tile with the tile in the new position . 
        new_state[blank], new_state[new_pos] = new_state[new_pos], new_state[blank]          # swapping the positions of blank . 
        neighbors.append(tuple(new_state))                                                      #adding the new state to the list of neighbors . 

    return neighbors

def a_star(start, goal):
    open_list = [start]
    came_from = {}
    g_cost = {start: 0}
    visited = set()

    while open_list:
        current = min(open_list, key=lambda x: g_cost[x] + heuristic(x, goal))
        open_list.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current)

        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            new_g = g_cost[current] + 1

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = new_g

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

print("Enter initial state (use 0 for blank)")
start = tuple(map(int, input().split()))

print("Enter goal state (use 0 for blank)")
goal = tuple(map(int, input().split()))

solution = a_star(start, goal)

if solution:
    print("\nSolution found in", len(solution) - 1, "moves\n")
    for step in solution:
        print_puzzle(step)
else:
    print("No solution found")
