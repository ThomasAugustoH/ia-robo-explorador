import networkx as nx
from collections import deque

class Robot:

    def __init__(self, starting_node, graph):
        self.robot_memory = nx.empty_graph()
        self.current_position = (starting_node)
        self.repeated_spaces = 0
        self.graph = graph
        self.current_path = []
        self.rotation_offset = 2

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
        for node in self.robot_memory.nodes():
            if self.get_node_status(node) == 'priority':
                self.current_path = self.__search_nodes(True)
                if len(self.current_path) == 2:
                    return
                else:
                    self.current_path = []
                    break
        
        for i in range(12):
            if i < 4:
                move = self.__get_next_move(self.rotation_offset, 'priority')
            elif i < 8:
                move = self.__get_next_move(self.rotation_offset, 'preferable')
            else:
                move = self.__get_next_move(self.rotation_offset)
            if move != ():
                break
            self.rotation_offset = (1 + self.rotation_offset) % 4
        if move != ():
            self.current_path.append(move)
        else:
            self.current_path = self.__search_nodes()

    def __move_to(self, node):
        for neighbor in self.robot_memory.neighbors(self.current_position):
            if self.get_node_status(neighbor) == 'unvisited':
                self.set_node_status(neighbor, 'unvisited')
        if self.get_node_status(node) == 'visited':
            self.repeated_spaces += 1
        self.set_node_status(self.current_position, 'visited')
        self.current_position = node
        self.set_node_status(node, 'current')
        self.__update_neighbors()

    def __search_nodes(self, close_distance=False) -> list:
        next_node = self.__find_closest_unvisited_node(close_distance)
        path = self.__find_path_to(next_node)
        return path

    def __find_closest_unvisited_node(self, close_distance) -> tuple:
        queue = deque([(self.current_position), 0])
        searched_nodes = {self.current_position}

        while queue:
            current_node = queue.popleft()
            distance = queue.popleft()

            if close_distance and distance > 2:
                return []

            for neighbor in self.robot_memory.neighbors(current_node):
                if neighbor not in searched_nodes:
                    searched_nodes.add(neighbor)

                    if self.get_node_status(neighbor) == 'priority':
                        return neighbor
                    
                    if self.get_node_status(neighbor) == 'preferable' and not close_distance:
                        return neighbor
                    
                    if self.get_node_status(neighbor) == 'unvisited' and not close_distance:
                        return neighbor
                    
                    queue.append(neighbor)
                    queue.append(distance + 1)

        return []

    def __find_path_to(self, destination) -> list:
        origin = self.current_position
        queue_path = deque([origin])
        predecessors = {origin: None} 
        path = []

        path_found = False

        while queue_path:
            current_node = queue_path.popleft()

            if current_node == destination:
                path_found = True
                break

            unvisited_neighbors = []
            visited_neighbors = []
            
            for neighbor in self.robot_memory.neighbors(current_node):
                if self.get_node_status(neighbor) in ['unvisited', 'preferable', 'priority']:
                    unvisited_neighbors.append(neighbor)
                else:
                    visited_neighbors.append(neighbor)

            for neighbor in unvisited_neighbors:
                if neighbor not in predecessors:
                    predecessors[neighbor] = current_node
                    queue_path.append(neighbor)
            
            for neighbor in visited_neighbors:
                if neighbor not in predecessors:
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
        if node in self.graph.nodes():
                if node not in self.robot_memory.nodes():
                    self.robot_memory.add_node(node, status = 'unvisited')
                if not self.get_node_status(node) == 'visited':
                    if self.graph.has_edge(self.current_position, node):
                        self.robot_memory.add_edge(self.current_position, node)
                        for neighbor in self.graph.neighbors(node):
                            if self.graph.has_edge(neighbor, node) and neighbor in self.robot_memory.nodes():
                                self.robot_memory.add_edge(neighbor, node)
                        self.set_node_status(node, self.__potential_dead_end(node))
                    else:
                        self.set_node_status(node, 'obstacle')
                        directions = ['EAST', 'SOUTH', 'WEST', 'NORTH']
                        robot_nodes = self.robot_memory.nodes()
                        for i in range(4):
                            neighbor = self.__get_node_position(node, directions[i])
                            if neighbor in robot_nodes:
                                if self.get_node_status(neighbor) == 'unvisited' or self.get_node_status(neighbor) == 'preferable':
                                    self.set_node_status(neighbor, self.__potential_dead_end(neighbor))
                    

    def __potential_dead_end(self, node) -> str:
        directions = ['EAST', 'SOUTH', 'WEST', 'NORTH']
        score = 0

        for i in range(4):
            next_node = self.__get_node_position(node, directions[i])
            if not next_node in self.graph.nodes():
                score += 2
            if next_node in self.robot_memory.nodes() and self.get_node_status(next_node) == 'obstacle':
                score += 2
            if next_node in self.robot_memory.nodes() and (self.get_node_status(next_node) == 'visited' or next_node == self.current_position):
                score += 1
            if score >= 4:
                return "priority"
        if score >= 2:
            return "preferable"
        return "unvisited"

    def __get_next_move(self, side, priority='unvisited') -> tuple:
        
        rotate_anti_clockwise = False
        side = (side + self.rotation_offset) % 4
        if rotate_anti_clockwise:
            if side == 0:
                side = 2
            elif side == 2:
                side = 0
        match self.rotation_offset:
            case 0:
                return self.__get_nearby_node('EAST', priority)
            case 1:
                return self.__get_nearby_node('SOUTH', priority)
            case 2:
                return self.__get_nearby_node('WEST', priority)
            case 3:
                return self.__get_nearby_node('NORTH', priority)
            
    def __get_nearby_node(self, direction, priority):
        next_node = self.__get_node_position(self.current_position, direction)
        if next_node in self.graph.nodes() and self.get_node_status(next_node) == priority:
            return next_node
        else:
            return ()
            
    def __get_node_position(self, node, direction):
        match direction:
            case 'EAST':
                x_offset, y_offset = 1, 0
            case 'SOUTH':
                x_offset, y_offset = 0, -1
            case 'WEST':
                x_offset, y_offset = -1, 0
            case 'NORTH':
                x_offset, y_offset = 0, 1
        next_node = (node[0] + x_offset, node[1] + y_offset)
        return next_node