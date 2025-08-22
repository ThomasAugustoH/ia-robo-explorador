import networkx as nx
import matplotlib.pyplot as plt

graph = nx.grid_2d_graph(10, 10)

def main():
    obstacle_list = create_obstacles(1)
    path = create_path((0,9), (7,2), obstacle_list)
    print_graph(path)

def create_path(source, destination, obstacles) -> list:
    path = find_path(source, destination)
    colored_path = color_path(path, obstacles)
    return colored_path

def find_path(source, destination) -> list:
    path = nx.dijkstra_path(graph, source, destination)
    return path

def color_path(path, obstacles) -> list:
    color_map = []
    for node in graph:
        if node in path:
            color_map.append('#aaeeaa')
        elif node in obstacles:
            color_map.append("#225C95")
        else:   
            color_map.append('#DDDDDD')
    return color_map

def print_graph(color_map):
    pos = {node: node for node in graph.nodes()}
    nx.draw_networkx(graph, pos=pos, node_color=color_map, node_shape='s', with_labels=False)
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