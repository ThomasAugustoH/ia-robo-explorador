import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from robot import Robot

class Environment:
    def __init__(self):
        self.graph_colors = {
            "current": "#FF7777",
            "visited": "#333333",
            "unvisited": "#AAAAAA",
            "priority": "#AAEEAA",
            "obstacle": "#225C95",
            "undiscovered_path": "#EEEEEE",
            "undiscovered_obstacle": "#90ADC9",
            "default": "#DDDDDD"
        }
        self.fig = None
        self.ax = None
        
    def run_simulation(self):
        plt.ion()
        self.set_settings()
        self.generate_map()
        self.create_robot()
        self.draw_map()

        has_moves_left = True
        while(has_moves_left):         
            has_moves_left = self.robot.move()
            self.draw_map()
                
        if self.should_draw_map:
            plt.ioff()
            plt.show()
        print(f"Passos redundantes: {self.robot.get_repeated_spaces()}")

    def set_settings(self):
        self.should_draw_map = self.wait_input('Do you want to draw the map? [Y] OR [N]: ')
        if self.should_draw_map:
            self.draw_only_robot_memory = self.wait_input('Do you want to draw only the map on the robot memory? [Y] OR [N]: ')
        self.preloaded_map = self.wait_input('Do you want to use the default map? [Y] OR [N]: ')
        self.debug_priority_enabled = True

    def generate_map(self):
        self.map_graph = nx.grid_2d_graph(10, 10)
        self.obstacle_list = []
        for node in self.map_graph.nodes():
            self.map_graph.nodes[node]['status'] = 'undiscovered_path'
        if self.preloaded_map:
            self.obstacle_list = self.create_obstacles(1)
        else:
            self.obstacle_list = self.create_obstacles()

    def draw_map(self):
        if not self.fig or not self.ax:
            self.fig, self.ax = plt.subplots(figsize=(8, 8))
        if self.should_draw_map:
            self.update_graph()
            plt.pause(2) 

    def wait_input(self, message) -> bool:
        while (True):
            response = input(message)
            if response.upper() not in ["Y", "N"]:
                print("Invalid input")
            else:
                break
        return response.upper() == "Y"

    def random_spawn_position(self) -> tuple:
        ignore_nodes = []
        has_path = False
        for node in self.map_graph.nodes():
            has_path = False
            for neighbor in self.map_graph.neighbors(node):
                if nx.has_path(self.map_graph, neighbor, node):
                    has_path = True
                    break
            if not has_path:
                ignore_nodes.append(node)
        
        possible_spawns = [node for node in self.map_graph.nodes() if node not in ignore_nodes]
        random_spawn = random.choice(possible_spawns)
        return random_spawn

    def create_robot(self):
        if self.preloaded_map:
            self.robot_pos = list((0, 9))
        else:
            self.robot_pos = list(self.random_spawn_position())
        print(f"Starting position: {tuple(self.robot_pos)}")
        self.robot = Robot(tuple(self.robot_pos), self.map_graph)
            
    def update_graph(self):
        self.ax.clear()

        self.robot_memory = self.robot.get_robot_memory()
        if self.draw_only_robot_memory:
            self.graph_to_draw = self.robot_memory
        else:
            self.graph_to_draw = self.map_graph

        pos = {node: node for node in self.graph_to_draw.nodes()}
        node_colors_map = []
        for node in self.graph_to_draw.nodes():
            if node in self.robot_memory.nodes():
                if self.robot.get_node_status(node)  == 'current':
                    node_colors_map.append(self.graph_colors.get("current"))
                elif self.robot.get_node_status(node)  == "visited":
                    node_colors_map.append(self.graph_colors.get("visited"))
                elif self.robot.get_node_status(node) == "unvisited":
                    node_colors_map.append(self.graph_colors.get("unvisited"))
                elif self.robot.get_node_status(node) == "priority":
                    node_colors_map.append(self.graph_colors.get("priority"))
                elif self.robot.get_node_status(node) == "obstacle":
                    node_colors_map.append(self.graph_colors.get("obstacle"))
                else:
                    node_colors_map.append(self.graph_colors.get("default"))
            else:
                if self.map_graph.nodes[node]['status'] == 'undiscovered_path':
                    node_colors_map.append(self.graph_colors.get('undiscovered_path'))
                elif self.map_graph.nodes[node]['status'] == 'undiscovered_obstacle':
                    node_colors_map.append(self.graph_colors.get('undiscovered_obstacle'))
                else:
                    node_colors_map.append(self.graph_colors.get("default"))
        nx.draw_networkx(self.graph_to_draw, pos=pos, node_color=node_colors_map, node_shape='s', with_labels=False)
        self.ax.set_title(f"Passos redundantes: {self.robot.get_repeated_spaces()}")
        self.ax.axis("off")
        plt.tight_layout()

    def create_obstacles(self, map=None) -> list:
        node_list = []
        if map != None:
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
                self.remove_edges_from_node(node)
        else:
            node_list = self.create_random_obstacles()

        return node_list

    def create_random_obstacles(self) -> list:
        number_of_obstacles = random.randint(20, 30)
        print(f"Gerando {number_of_obstacles} obstáculos")
        connected_components = 1
        created_objects = []
        for i in range(number_of_obstacles):
            creation_successful = False
            while not creation_successful:
                graph_copy = self.map_graph.copy()
                obstacle = random.choice(list(node for node in self.map_graph.nodes() if node not in created_objects))
                self.remove_edges_from_node(obstacle)
                new_connected_components = nx.number_connected_components(self.map_graph)
                if new_connected_components > connected_components + 1:
                    self.map_graph = graph_copy
                else:
                    connected_components += 1
                    creation_successful = True
                    created_objects.append(obstacle)
        return created_objects

    def remove_edges_from_node(self, node):
        self.map_graph.nodes[node]['status'] = 'undiscovered_obstacle'
        edges = list(self.map_graph.edges(node))
        self.map_graph.remove_edges_from(edges)