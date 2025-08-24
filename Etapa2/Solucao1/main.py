import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from robot import Robot

graph = nx.grid_2d_graph(10, 10)

obstacle_list = []
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
robot = None

def main():
    global draw_graph
    draw_graph = wait_input("Do you want to draw the graph? [Y] OR [N]: ")
    global obstacle_list
    obstacle_list = create_obstacles(1)
    global robot 
    robot = create_robot()
    if draw_graph:
        update_graph(robot.get_robot_memory())

    has_moves_left = True
    while(has_moves_left):         
        has_moves_left = robot.move()
        if draw_graph:
            update_graph(robot.get_robot_memory())

    print(f"Passos redundantes: {robot.get_repeated_spaces()}")



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
    global graph
    
    randomize_starting_pos = wait_input("Do you want to randomize the starting position? [Y] OR [N]: ")

    if randomize_starting_pos:
        robot_pos = list(random_spawn_position())
    else:
        robot_pos = list((0, 9))
    print(f"Starting position: {tuple(robot_pos)}")
    robot = Robot(tuple(robot_pos), graph)

    return robot
    
    

### AUXILIARY FUNCTIONS ---------------------------------------------------------------------------

def update_graph(graph):
    plt.close()
    global graph_colors
    global robot
    robot_memory = robot.get_robot_memory()

    pos = {node: node for node in graph.nodes()}
    node_colors_map = []
    for node in graph.nodes():
        if tuple(robot.get_current_position()) == node:
            node_colors_map.append(graph_colors.get("current_pos"))
        elif robot_memory.nodes[node]['status']  == "visited":
            node_colors_map.append(graph_colors.get("visited"))
        elif robot_memory.nodes[node]['status'] == "unvisited":
            node_colors_map.append(graph_colors.get("unvisited"))
        elif robot_memory.nodes[node]['status'] == "priority":
            node_colors_map.append(graph_colors.get("priority"))
        elif robot_memory.nodes[node]['status'] == "obstacle":
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