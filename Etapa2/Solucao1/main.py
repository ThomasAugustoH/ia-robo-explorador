import random
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

graph = nx.grid_2d_graph(10, 10)
flags = {}
robot_pos = []
obstacle_list = []
robot_memory = nx.empty_graph()
repeated_spaces = 0
draw_graph = False
graph_colors = {
    "current_pos": "#FF7777",
    "visited": "#333333",
    "unvisited": "#AAAAAA",
    "priority": "#AAEEAA",
    "obstacle": "#225C95",
    "default": "#DDDDDD"
}

def main():
    global draw_graph
    draw_graph = wait_input("Do you want to draw the graph? [Y] OR [N]: ")
    global obstacle_list
    obstacle_list = create_obstacles(1)
    create_robot()
    if draw_graph:
        update_graph(robot_memory)

    has_moves_left = True
    while(has_moves_left):         
        has_moves_left = move()

    print(f"Passos redundantes: {repeated_spaces}")




### SETUP ---------------------------------------------------------------------------

def wait_input(message) -> bool:
    while (True):
        response = input(message)

        if response.upper() not in ["Y", "N"]:
            print("Invalid input")
        else:
            break
    return response.upper() == "Y"

def random_spawn_position() -> tuple:
    ignore_nodes = []
    has_path = False
    for node in graph.nodes():
        has_path = False
        for neighbor in graph.neighbors(node):
            if nx.has_path(graph, neighbor, node):
                has_path = True
                break
        if not has_path:
            ignore_nodes.append(node)
    
    possible_spawns = [node for node in graph.nodes() if node not in ignore_nodes]
    random_spawn = random.choice(possible_spawns)
    return random_spawn

def create_robot():
    global robot_pos
    global robot_memory

    randomize_starting_pos = wait_input("Do you want to randomize the starting position? [Y] OR [N]: ")

    if randomize_starting_pos:
        robot_pos = list(random_spawn_position())
    else:
        robot_pos = list((0, 9))
    print(f"Starting position: {tuple(robot_pos)}")
    robot_memory.add_node(tuple(robot_pos))
    flags[tuple(robot_pos)] = "visited"
    update_neighbors()



### ROBOT CODE ---------------------------------------------------------------------------

def move() -> bool:
    move_sequence = []
    
    for i in range(8):
        if i < 4:
            move = get_next_move(i, True)
        else:
            move = get_next_move(i-4)
        if move != ():
            break
    if move != ():
        move_sequence.append(move)
    else:
        move_sequence = search_nodes()

    if move_sequence == []:
        return False

    global robot_pos
    global repeated_spaces
    global draw_graph
    for node in move_sequence:
        for neighbors in robot_memory.neighbors(tuple(robot_pos)):
            if flags[neighbors] == "unvisited":
                flags[neighbors] = "priority"
        if flags[node] == "visited":
            repeated_spaces += 1
        robot_pos = list(node)
        flags[node] = "visited"
        update_neighbors()
        if draw_graph:
            update_graph(robot_memory)

    return True

def search_nodes() -> list:
    next_node = find_closest_unvisited_node()
    path = find_path_to(next_node)
    return path

def find_closest_unvisited_node() -> tuple:
    queue = deque([(tuple(robot_pos)), 0])
    searched_nodes = {tuple(robot_pos)}
    unvisited_node = []

    while queue:
        current_node = queue.popleft()
        distance = queue.popleft()

        for neighbor in robot_memory.neighbors(current_node):
            if neighbor not in searched_nodes:
                searched_nodes.add(neighbor)

                if flags[neighbor] == "priority":
                    return neighbor
                
                if flags[neighbor] == "unvisited":
                    unvisited_node = list(neighbor)
                
                queue.append(neighbor)
                queue.append(distance + 1)

    return tuple(unvisited_node)

def find_path_to(destination) -> list:
    origin = tuple(robot_pos)
    queue_path = deque([origin])
    predecessors = {node: None for node in robot_memory.nodes}
    visited_path = {origin}
    path = []

    path_found = False

    while queue_path:
        current_node = queue_path.popleft()

        if current_node == destination:
            path_found = True
            break

        for neighbor in robot_memory.neighbors(current_node):
            if neighbor not in visited_path:
                visited_path.add(neighbor)
                predecessors[neighbor] = current_node
                queue_path.append(neighbor)

    if path_found:
        current = destination
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]
        path.remove(origin)
    return path

def update_neighbors():
    next_node = (robot_pos[0] + 1, robot_pos[1])
    update_neighbor(next_node)
    next_node = (robot_pos[0], robot_pos[1] - 1)
    update_neighbor(next_node)
    next_node = (robot_pos[0] - 1, robot_pos[1])
    update_neighbor(next_node)
    next_node = (robot_pos[0], robot_pos[1] + 1)
    update_neighbor(next_node)

def update_neighbor(node):
    if node in graph.nodes() and node not in robot_memory.nodes():
            robot_memory.add_node(node)
            if nx.has_path(graph, tuple(robot_pos), node):
                robot_memory.add_edge(tuple(robot_pos), node)
                for neighbor in graph.neighbors(node):
                    if nx.has_path(graph, neighbor, node) and neighbor in robot_memory.nodes():
                        robot_memory.add_edge(neighbor, node)
                flags[tuple(node)] = "unvisited"
            else:
                flags[tuple(node)] = "obstacle"

def get_next_move(side, look_for_priority = False) -> tuple:
    rotation_offset = 2
    rotate_anti_clockwise = True
    side = (side + rotation_offset) % 4
    if rotate_anti_clockwise:
        match side:
            case 0:
                return get_west_node(look_for_priority)
            case 1:
                return get_south_node(look_for_priority)
            case 2:
                return get_east_node(look_for_priority)
            case 3:
                return get_north_node(look_for_priority)
    else:
        match side:
            case 0:
                return get_east_node(look_for_priority)
            case 1:
                return get_south_node(look_for_priority)
            case 2:
                return get_west_node(look_for_priority)
            case 3:
                return get_north_node(look_for_priority)

def get_east_node(look_for_priority = False) -> tuple:
    next_node = (robot_pos[0] + 1, robot_pos[1])
    if look_for_priority:
        if next_node in robot_memory.nodes() and flags[tuple(next_node)] == "priority":
            return next_node
        else:
            return ()
    else: 
        if next_node in robot_memory.nodes() and flags[tuple(next_node)] == "unvisited":
            return next_node
        else:
            return ()

def get_south_node(look_for_priority = False) -> tuple:
    next_node = (robot_pos[0], robot_pos[1] - 1)
    if look_for_priority:
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "priority":
            return next_node
        else:
            return ()
    else: 
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "unvisited":
            return next_node
        else:
            return ()
    
def get_west_node(look_for_priority = False) -> tuple:
    next_node = (robot_pos[0] - 1, robot_pos[1])
    if look_for_priority:
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "priority":
            return next_node
        else:
            return ()
    else: 
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "unvisited":
            return next_node
        else:
            return ()
    
def get_north_node(look_for_priority = False) -> tuple:
    next_node = (robot_pos[0], robot_pos[1] + 1)
    if look_for_priority:
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "priority":
            return next_node
        else:
            return ()
    else: 
        if next_node in graph.nodes() and next_node not in obstacle_list and flags[tuple(next_node)] == "unvisited":
            return next_node
        else:
            return ()



### AUXILIARY FUNCTIONS ---------------------------------------------------------------------------

def update_graph(graph):
    plt.close()
    global graph_colors

    pos = {node: node for node in graph.nodes()}
    node_colors_map = []
    for node in graph.nodes():
        if tuple(robot_pos) == node:
            node_colors_map.append(graph_colors.get("current_pos"))
        elif flags[node] == "visited":
            node_colors_map.append(graph_colors.get("visited"))
        elif flags[node] == "unvisited":
            node_colors_map.append(graph_colors.get("unvisited"))
        elif flags[node] == "priority":
            node_colors_map.append(graph_colors.get("priority"))
        elif flags[node] == "obstacle":
            node_colors_map.append(graph_colors.get("obstacle"))
        else:
            node_colors_map.append(graph_colors.get("default"))
    nx.draw_networkx(graph, pos=pos, node_color=node_colors_map, node_shape='s', with_labels=False)
    plt.tight_layout()
    plt.axis("off")
    plt.show()

def create_obstacles(map) -> list:
    node_list = []
    
    match map:
        case 1:
            node_list.append((5, 0))
            node_list.append((5, 1))
            node_list.append((7, 1))
            node_list.append((8, 1))
            node_list.append((5, 2))
            node_list.append((8, 2))
            node_list.append((5, 3))
            node_list.append((8, 3))
            node_list.append((3, 4))
            node_list.append((5, 4))
            node_list.append((6, 4))
            node_list.append((7, 4))
            node_list.append((8, 4))
            node_list.append((1, 5))
            node_list.append((6, 5))
            node_list.append((2, 6))
            node_list.append((5, 6))
            node_list.append((2, 7))
            node_list.append((0, 8))
            node_list.append((3, 8))
            node_list.append((4, 9))

    for node in node_list:
        remove_edges_from_node(node)

    return node_list

def remove_edges_from_node(node):
    edges = list(graph.edges(node))
    graph.remove_edges_from(edges)

if __name__ == "__main__":
    main()