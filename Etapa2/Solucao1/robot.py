import networkx as nx
from collections import deque

class Robot:

    def __init__(self, starting_node, graph):
        self.robot_memory = nx.empty_graph()
        self.current_position = (starting_node)
        self.repeated_spaces = 0
        self.graph = graph
        self.current_path = []

        self.robot_memory.add_node(self.current_position, status='current')
        self.__update_neighbors()

    def get_robot_memory(self):
        return self.robot_memory
    
    def get_current_position(self):
        return self.current_position
    
    def get_repeated_spaces(self):
        return self.repeated_spaces
    
    def set_node_status(self, node, status):
        self.robot_memory.nodes[node]['status'] = status

    def get_node_status(self, node) -> str:
        return self.robot_memory.nodes[node]['status']
    
    def move(self) -> bool:
        if len(self.current_path) == 0:
            self.__find_next_path()
        if len(self.current_path) > 0:
            self.__move_to(self.current_path.pop(0))
            return True
        return False
        
    def __find_next_path(self):
        for i in range(8):
            if i < 4:
                move = self.__get_next_move(i, True)
            else:
                move = self.__get_next_move(i-4)
            if move != ():
                break
        if move != ():
            self.current_path.append(move)
        else:
            self.current_path = self.__search_nodes()

    def __move_to(self, node):
        for neighbor in self.robot_memory.neighbors(self.current_position):
            if self.get_node_status(neighbor) == 'unvisited':
                self.set_node_status(neighbor, 'priority')
        if self.get_node_status(node) == 'visited':
            self.repeated_spaces += 1
        self.set_node_status(self.current_position, 'visited')
        self.current_position = node
        self.set_node_status(node, 'current')
        self.__update_neighbors()

    def __search_nodes(self) -> list:
        next_node = self.__find_closest_unvisited_node()
        path = self.__find_path_to(next_node)
        return path

    def __find_closest_unvisited_node(self) -> tuple:
        queue = deque([(self.current_position), 0])
        searched_nodes = {self.current_position}
        unvisited_node = []

        while queue:
            current_node = queue.popleft()
            distance = queue.popleft()

            for neighbor in self.robot_memory.neighbors(current_node):
                if neighbor not in searched_nodes:
                    searched_nodes.add(neighbor)

                    if self.get_node_status(neighbor) == 'priority':
                        return neighbor
                    
                    if self.get_node_status(neighbor) == 'unvisited' and unvisited_node == []:
                        unvisited_node = list(neighbor)
                    
                    queue.append(neighbor)
                    queue.append(distance + 1)

        return tuple(unvisited_node)

    def __find_path_to(self, destination) -> list:
        origin = self.current_position
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

    def __update_neighbors(self):
        next_node = (self.current_position[0] + 1, self.current_position[1])
        self.__update_neighbor(next_node)
        next_node = (self.current_position[0], self.current_position[1] - 1)
        self.__update_neighbor(next_node)
        next_node = (self.current_position[0] - 1, self.current_position[1])
        self.__update_neighbor(next_node)
        next_node = (self.current_position[0], self.current_position[1] + 1)
        self.__update_neighbor(next_node)

    def __update_neighbor(self, node):
        if node in self.graph.nodes() and node not in self.robot_memory.nodes():
                self.robot_memory.add_node(node, status = 'unvisited')
                if nx.has_path(self.graph, self.current_position, node):
                    self.robot_memory.add_edge(self.current_position, node, )
                    for neighbor in self.graph.neighbors(node):
                        if nx.has_path(self.graph, neighbor, node) and neighbor in self.robot_memory.nodes():
                            self.robot_memory.add_edge(neighbor, node)
                else:
                    self.set_node_status(node, 'obstacle')

    def __get_next_move(self, side, look_for_priority = False) -> tuple:
        rotation_offset = 2
        rotate_anti_clockwise = True
        side = (side + rotation_offset) % 4
        if rotate_anti_clockwise:
            if side == 0:
                side = 2
            elif side == 2:
                side = 0
        match side:
            case 0:
                return self.__get_nearby_node('EAST', look_for_priority)
            case 1:
                return self.__get_nearby_node('SOUTH', look_for_priority)
            case 2:
                return self.__get_nearby_node('WEST', look_for_priority)
            case 3:
                return self.__get_nearby_node('NORTH', look_for_priority)
            
    def __get_nearby_node(self, direction, look_for_priority = False):
        match direction:
            case 'EAST':
                x_offset, y_offset = 1, 0
            case 'SOUTH':
                x_offset, y_offset = 0, -1
            case 'WEST':
                x_offset, y_offset = -1, 0
            case 'NORTH':
                x_offset, y_offset = 0, 1

        next_node = (self.current_position[0] + x_offset, self.current_position[1] + y_offset)
        if look_for_priority:
            if next_node in self.graph.nodes() and self.get_node_status(next_node) == 'priority':
                return next_node
            else:
                return ()
        else: 
            if next_node in self.graph.nodes() and self.get_node_status(next_node) == 'unvisited':
                return next_node
            else:
                return ()