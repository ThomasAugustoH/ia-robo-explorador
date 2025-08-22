import networkx as nx
import matplotlib.pyplot as plt

def main():
    grid = nx.grid_2d_graph(10, 10)
   
    remove_nodes(grid, 1)
    path = create_path(grid, (0,9), (7,2))
    print_graph(grid, path)

def create_path(graph, source, destination) -> list:
    path = find_path(graph, source, destination)
    colored_path = color_path(graph, path)
    return colored_path

def find_path(graph, source, destination) -> list:
    path = nx.dijkstra_path(graph, source, destination)
    return path

def color_path(graph, path) -> list:
    color_map = []
    for node in graph:
        if node in path:
            color_map.append('#F08C01')
        else:
            color_map.append('#DDDDDD')
    return color_map

def print_graph(graph, color_map):
    pos = {node: node for node in graph.nodes()}
    nx.draw_networkx(graph, pos=pos, node_color=color_map, with_labels=False)
    plt.tight_layout()
    plt.axis("off")
    plt.show()

def remove_nodes(graph, map):
    match map:
        case 1:
            graph.remove_node((5, 0))
            graph.remove_node((5, 1))
            graph.remove_node((7, 1))
            graph.remove_node((8, 1))
            graph.remove_node((5, 2))
            graph.remove_node((8, 2))
            graph.remove_node((5, 3))
            graph.remove_node((8, 3))
            graph.remove_node((3, 4))
            graph.remove_node((5, 4))
            graph.remove_node((6, 4))
            graph.remove_node((7, 4))
            graph.remove_node((8, 4))
            graph.remove_node((1, 5))
            graph.remove_node((6, 5))
            graph.remove_node((2, 6))
            graph.remove_node((5, 6))
            graph.remove_node((2, 7))
            graph.remove_node((0, 8))
            graph.remove_node((3, 8))
            graph.remove_node((4, 9))

if __name__ == "__main__":
    main()