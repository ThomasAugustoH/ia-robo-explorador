from robot import Robot


rows, coluns = 10, 10
grid = [[0] * coluns for _ in range(rows)]

robot = Robot(grid, 0, 0)

while robot.direction < 5:
    while robot.can_move_forward():
        robot.move_forward()
    robot.rotate()

print("Hitted all four walls")
