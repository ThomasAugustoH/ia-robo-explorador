import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from environment import Environment


def main():
    environment = Environment()
    environment.run_simulation()

if __name__ == "__main__":
    main()