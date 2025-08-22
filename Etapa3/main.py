import networkx as nx
import matplotlib.pyplot as plt



def main():
    grid = nx.grid_2d_graph(10, 10)
    list(nx.connected_components(grid))
    pos = {node: node for node in grid.nodes()}

    remove_nodes(grid, 1)

    path = find_path(grid, (0,9), (7,2))
    unaccessed_nodes = list(grid.nodes)

    print(unaccessed_nodes)

    nx.draw_networkx_nodes(grid, pos=pos, nodelist=path, node_color="tab:red")

    nx.draw(grid, pos=pos, with_labels=True, font_weight='bold')
    plt.show()

def find_path(graph, source, destination) :
    path = nx.dijkstra_path(graph, source, destination)
    return path

def remove_nodes(grid, map):
    match map:
        case 1:
            grid.remove_node((5, 0))
            grid.remove_node((5, 1))
            grid.remove_node((7, 1))
            grid.remove_node((8, 1))
            grid.remove_node((5, 2))
            grid.remove_node((8, 2))
            grid.remove_node((5, 3))
            grid.remove_node((8, 3))
            grid.remove_node((3, 4))
            grid.remove_node((5, 4))
            grid.remove_node((6, 4))
            grid.remove_node((7, 4))
            grid.remove_node((8, 4))
            grid.remove_node((1, 5))
            grid.remove_node((6, 5))
            grid.remove_node((2, 6))
            grid.remove_node((5, 6))
            grid.remove_node((2, 7))
            grid.remove_node((0, 8))
            grid.remove_node((3, 8))
            grid.remove_node((4, 9))

if __name__ == "__main__":
    main()