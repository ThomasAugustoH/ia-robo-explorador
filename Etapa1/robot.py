class Robot:


    def __init__(self, grid, x, y):
        self.grid = grid
        self.position = (x, y)
        self.direction = 1

    def get_movement_based_on_direction(self):
        x, y = self.position

        if self.direction == 1:
            return  x, y + 1
        elif self.direction == 2:
            return x + 1, y
        elif self.direction == 3:
            return x, y - 1
 
        return x - 1, y

    def can_move_forward(self):
        x, y = self.get_movement_based_on_direction()
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return True

        return False

    def move_forward(self):
        self.position = self.get_movement_based_on_direction()

    def rotate(self):
        self.direction = self.direction + 1

