import networkx as nx
from collections import deque

class Robot:

    def __init__(self, starting_node, graph):
        self.robot_memory = nx.empty_graph()
        self.current_position = (starting_node)
        self.repeated_spaces = 0
        self.flags = {}
        self.graph = graph

        self.robot_memory.add_node(tuple(self.current_position))
        self.flags[tuple(self.current_position)] = "visited"
        self.update_neighbors()

    def get_robot_memory(self):
        return self.robot_memory

    def get_robot_flags(self):
        return self.flags
    
    def get_current_position(self):
        return self.current_position
    
    def get_repeated_spaces(self):
        return self.repeated_spaces

    def move(self) -> bool:
        move_sequence = []
        
        for i in range(8):
            if i < 4:
                move = self.get_next_move(i, True)
            else:
                move = self.get_next_move(i-4)
            if move != ():
                break
        if move != ():
            move_sequence.append(move)
        else:
            move_sequence = self.search_nodes()

        if move_sequence == []:
            return False

        for node in move_sequence:
            for neighbors in self.robot_memory.neighbors(tuple(self.current_position)):
                if self.flags[neighbors] == "unvisited":
                    self.flags[neighbors] = "priority"
            if self.flags[node] == "visited":
                self.repeated_spaces += 1
            self.current_position = list(node)
            self.flags[node] = "visited"
            self.update_neighbors()

        return True

    def search_nodes(self) -> list:
        next_node = self.find_closest_unvisited_node()
        path = self.find_path_to(next_node)
        return path

    def find_closest_unvisited_node(self) -> tuple:
        queue = deque([(tuple(self.current_position)), 0])
        searched_nodes = {tuple(self.current_position)}
        unvisited_node = []

        while queue:
            current_node = queue.popleft()
            distance = queue.popleft()

            for neighbor in self.robot_memory.neighbors(current_node):
                if neighbor not in searched_nodes:
                    searched_nodes.add(neighbor)

                    if self.flags[neighbor] == "priority":
                        return neighbor
                    
                    if self.flags[neighbor] == "unvisited":
                        unvisited_node = list(neighbor)
                    
                    queue.append(neighbor)
                    queue.append(distance + 1)

        return tuple(unvisited_node)

    def find_path_to(self, destination) -> list:
        origin = tuple(self.current_position)
        queue_path = deque([origin])
        predecessors = {node: None for node in self.robot_memory.nodes}
        visited_path = {origin}
        path = []

        path_found = False

        while queue_path:
            current_node = queue_path.popleft()

            if current_node == destination:
                path_found = True
                break

            for neighbor in self.robot_memory.neighbors(current_node):
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

    def update_neighbors(self):
        next_node = (self.current_position[0] + 1, self.current_position[1])
        self.update_neighbor(next_node)
        next_node = (self.current_position[0], self.current_position[1] - 1)
        self.update_neighbor(next_node)
        next_node = (self.current_position[0] - 1, self.current_position[1])
        self.update_neighbor(next_node)
        next_node = (self.current_position[0], self.current_position[1] + 1)
        self.update_neighbor(next_node)

    def update_neighbor(self, node):
        if node in self.graph.nodes() and node not in self.robot_memory.nodes():
                self.robot_memory.add_node(node)
                if nx.has_path(self.graph, tuple(self.current_position), node):
                    self.robot_memory.add_edge(tuple(self.current_position), node)
                    for neighbor in self.graph.neighbors(node):
                        if nx.has_path(self.graph, neighbor, node) and neighbor in self.robot_memory.nodes():
                            self.robot_memory.add_edge(neighbor, node)
                    self.flags[tuple(node)] = "unvisited"
                else:
                    self.flags[tuple(node)] = "obstacle"

    def get_next_move(self, side, look_for_priority = False) -> tuple:
        rotation_offset = 2
        rotate_anti_clockwise = True
        side = (side + rotation_offset) % 4
        if rotate_anti_clockwise:
            match side:
                case 0:
                    return self.get_nearby_node("WEST", look_for_priority)
                case 1:
                    return self.get_nearby_node("SOUTH", look_for_priority)
                case 2:
                    return self.get_nearby_node("EAST", look_for_priority)
                case 3:
                    return self.get_nearby_node("NORTH", look_for_priority)
        else:
            match side:
                case 0:
                    return self.get_nearby_node("EAST", look_for_priority)
                case 1:
                    return self.get_nearby_node("SOUTH", look_for_priority)
                case 2:
                    return self.get_nearby_node("WEST", look_for_priority)
                case 3:
                    return self.get_nearby_node("NORTH", look_for_priority)
            
    def get_nearby_node(self, direction, look_for_priority = False):
        match direction:
            case "EAST":
                x_offset, y_offset = 1, 0
            case "SOUTH":
                x_offset, y_offset = 0, -1
            case "WEST":
                x_offset, y_offset = -1, 0
            case "NORTH":
                x_offset, y_offset = 0, 1

        next_node = (self.current_position[0] + x_offset, self.current_position[1] + y_offset)
        if look_for_priority:
            if next_node in self.graph.nodes() and self.flags[tuple(next_node)] == "priority":
                return next_node
            else:
                return ()
        else: 
            if next_node in self.graph.nodes() and self.flags[tuple(next_node)] == "unvisited":
                return next_node
            else:
                return ()