import matplotlib
matplotlib.use("TkAgg")
import networkx as nx
import matplotlib.pyplot as plt

grid = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,3,1,1,1,1],
    [1,1,2,2,1,3,3,2,1,1],
    [1,1,2,1,3,3,3,2,1,1],
    [1,1,2,2,3,3,3,2,2,1],
    [1,1,1,2,3,1,2,2,1,1],
    [1,1,1,1,2,3,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
]

ROWS = len(grid)
COLS = len(grid[0])

color_by_weight = {1: "#16D100", 2: "#FFF400", 3: "#ff0000"}

def build_graph_from_grid(grid):
    G = nx.DiGraph()
    for row in range(ROWS):
        for column in range(COLS):
            G.add_node((row, column), weight=grid[row][column])

    return create_edges_with_weights(G)

def create_edges_with_weights(G):
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for current_row in range(ROWS):
        for current_column in range(COLS):
            for direction_row, direction_column in directions:
                new_edge_row = current_row + direction_row
                new_edge_column = current_column + direction_column

                if 0 <= new_edge_row < ROWS and 0 <= new_edge_column < COLS:
                    G.add_edge(
                        (current_row, current_column),
                        (new_edge_row, new_edge_column),
                        weight=grid[new_edge_row][new_edge_column]
                    )

    return G

def calculate_next_node(G, current_node, target):
    neighbors = list(G.neighbors(current_node))
    if not neighbors:
        return None
    
    lowest_cost = float('inf')
    best_node = None
    
    for node in neighbors:
        cost = distance_from_target(G, current_node,target, node)
        if cost < lowest_cost:
            lowest_cost = cost
            best_node = node

    return best_node

def distance_from_target(G, current_node, target, node):
    distance = abs(node[0] - target[0]) + abs(node[1] - target[1])

    weight = G.edges[current_node, node]["weight"]
    return distance + weight

def draw(G, path):
    pos = {n: n for n in G.nodes()}
    node_list = list(G.nodes())
    node_colors = [color_by_weight.get(G.nodes[n]['weight'], "#999999") for n in node_list]

    plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_color=node_colors, node_shape='s', node_size=100)

    undirected = list({tuple(sorted((u,v))) for u,v in G.edges()})
    nx.draw_networkx_edges(G, pos, edgelist=undirected, edge_color="#CCCCCC", width=1, arrows=False)

    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        widths = [G[u][v]['weight'] + 1.5 for u,v in path_edges]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="#0066FF", width=widths, arrows=True,  arrowsize=12)

    plt.gca().set_axis_off()
    plt.tight_layout()
    plt.show()

def main():
    G = build_graph_from_grid(grid)
    source = (0,5)
    target = (9,5)
    current_node = source
    cost = 0
    path = [current_node]

    while current_node != target:
        next_node = calculate_next_node(G, current_node, target)
        current_node = next_node
        cost += G.nodes[current_node]['weight']
        path.append(current_node)
        draw(G, path)

    print("Custo total:", cost)
if __name__ == "__main__":
    main()
