import random as rnd
from robot import Robot


rows, coluns = 10, 10
grid = [[0] * coluns for _ in range(rows)]

start_x = rnd.randint(0, coluns - 1)
start_y = rnd.randint(0, rows - 1)

print(f"Robô iniciando na posição aleatória: ({start_x}, {start_y})")

robot = Robot(grid, start_x, start_y)

while robot.direction < 5:
    while robot.can_move_forward():
        robot.move_forward()
    robot.rotate()

print("Hitted all four walls")