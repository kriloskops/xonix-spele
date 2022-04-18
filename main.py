from time import sleep
from tkinter import *
import random
from turtle import update



WIN_HEIGHT = 1000
WIN_WITDH = 1000



master = Tk()
canv = Canvas(master, height=WIN_HEIGHT, width=WIN_WITDH)

GRID_WIDTH = 30
GRID_HEIGHT = 30

img = PhotoImage(width=WIN_WITDH, height=WIN_HEIGHT)
canv.create_image( 0, 0, image=img, anchor=NW )
# GRID = [[0 for i in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]
# for i in range(len(GRID)):
#     for j in range(len(GRID[0])):
#         if (i == 0 or j == 0 or i == GRID_WIDTH - 1 or j == GRID_HEIGHT - 1 or (random.randint(1, 75) == 15)):
#             GRID[i][j] = 1


# for i in range(len(GRID)):
#     for j in range(len(GRID[0])):
#         if (GRID[i][j] == 1):
#             canv.create_rectangle(WIN_WITDH / GRID_WIDTH * i, WIN_HEIGHT / GRID_HEIGHT * j , WIN_WITDH / GRID_WIDTH * i + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * j + WIN_HEIGHT / GRID_HEIGHT, fill = "black")




#WIN_WITDH / GRID_WIDTH * i, WIN_HEIGHT / GRID_HEIGHT * j , WIN_WITDH / GRID_WIDTH * i + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * j + WIN_HEIGHT / GRID_HEIGHT

#lambda color, column=i, row=j : img.put(color, (WIN_WITDH / GRID_WIDTH * i, WIN_HEIGHT / GRID_HEIGHT * j , WIN_WITDH / GRID_WIDTH * i + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * j + WIN_HEIGHT / GRID_HEIGHT))

class Grid1:
    def __init__(self, width, height):
        #self.grid = [[[0, canv.create_rectangle(WIN_WITDH / GRID_WIDTH * i, WIN_HEIGHT / GRID_HEIGHT * j , WIN_WITDH / GRID_WIDTH * i + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * j + WIN_HEIGHT / GRID_HEIGHT)] for j in range(width)] for i in range(height)]
        self.grid = [[[0, lambda color, column=i, row=j : img.put(color, (int(WIN_WITDH / GRID_WIDTH * column), int(WIN_HEIGHT / GRID_HEIGHT * row), int(WIN_WITDH / GRID_WIDTH * column + WIN_WITDH / GRID_WIDTH), int(WIN_HEIGHT / GRID_HEIGHT * row + WIN_HEIGHT / GRID_HEIGHT)))] for j in range(width)] for i in range(height)]

        
        self.height = height
        self.width = width


        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if (i == 0 or j == 0 or i == width - 1 or j == height - 1):
                    self.grid[i][j][0] = 1
                    self.grid[i][j][1]("black")

        self.player = ()

        self.runners = []
        
        canv.pack()


    def get_cube(self, i, j):
        return self.grid[i][j][0]

    def create_player(self, x, y):
        id = canv.create_rectangle(WIN_WITDH / self.width * x, WIN_HEIGHT / self.height * y , WIN_WITDH / self.width * x + WIN_WITDH / self.width, WIN_HEIGHT / self.height * y + WIN_HEIGHT / self.height, fill="lime")
        self.player = (x, y, id)
        return id


    def move_player(self, x, y):
        canv.coords(self.player[2], WIN_WITDH / self.width * x, WIN_HEIGHT / self.height * y , WIN_WITDH / self.width * x + WIN_WITDH / self.width, WIN_HEIGHT / self.height * y + WIN_HEIGHT / self.height)


    def create_runner(self, x, y):
        id = canv.create_rectangle(WIN_WITDH / self.width * x, WIN_HEIGHT / self.height * y , WIN_WITDH / self.width * x + WIN_WITDH / self.width, WIN_HEIGHT / self.height * y + WIN_HEIGHT / self.height, fill = "red")
        self.runners.append((x, y, id))
        return id

    def move_runner(self, id, x, y):
        canv.coords(id, WIN_WITDH / self.width * x, WIN_HEIGHT / self.height * y , WIN_WITDH / self.width * x + WIN_WITDH / self.width, WIN_HEIGHT / self.height * y + WIN_HEIGHT / self.height)

    def get_random_loc(self):
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        while (self.grid[x][y][0] != 0):
            x = random.randint(1, GRID_WIDTH)
            y = random.randint(1, GRID_HEIGHT)

        return x, y





    def setPath(self, x, y):
        self.grid[x][y][0] = 2
        self.grid[x][y][1]("gray")

    
    def fill_dfs(self, x, y):
        if (self.get_cube(x, y) != 0):
            return 
        
        self.grid[x][y][0] = 3
        # self.grid[x][y][1]("yellow")
        
        self.fill_dfs(x + 1, y)
        self.fill_dfs(x - 1, y)
        self.fill_dfs(x, y + 1)
        self.fill_dfs(x, y - 1)



    def fill(self):
        for i in self.runners:
            self.fill_dfs(i[1], i[0])

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if (self.grid[i][j][0] == 0 or self.grid[i][j][0] == 2):
                    self.grid[i][j][0] = 1
                    self.grid[i][j][1]("black")
                elif (self.grid[i][j][0] == 3):
                    self.grid[i][j][0] = 0
                    # self.grid[i][j][1]("yellow")

        # for i in self.grid:
        #     print(list(map(lambda x: x[0], i)))
    

class Runner:
    
    grid : Grid1 = None
    	
    
    @staticmethod
    def set_grid(gridi):
        grid = gridi


    def __init__(self, x = None, y = None):
        global grid
        rl = grid.get_random_loc()
        if (x == None):
            x = rl[0]
            y = rl[1]


        grid = grid
        self.x = x
        self.y = y
        self.dx = 1 if (random.randint(0, 1)) else -1
        self.dy = 1 if (random.randint(0, 1)) else -1


        self.rect = grid.create_runner(x, y)
        

    def move(self):

        bef = [self.dx, self.dy]
        if (grid.get_cube(self.x + 1, self.y) == 1):
            self.dx = -1
        if (grid.get_cube(self.x - 1, self.y) == 1):
            self.dx = 1
        if (grid.get_cube(self.x, self.y + 1) == 1):
            self.dy = -1
        if (grid.get_cube(self.x, self.y - 1) == 1):
            self.dy = 1

        if ([self.dx, self.dy] == bef):
            if (grid.get_cube(self.x + self.dx, self.y + self.dy) == 1):
                if (self.dx == 1):
                    self.dx = -1
                else:
                    self.dx = 1
                if (self.dy == 1):
                    self.dy = -1
                else:
                    self.dy = 1
        
        grid.grid[self.x][self.y][0] = 0
        self.x += self.dx
        self.y += self.dy
        #grid.grid[self.x][self.y][0] = 2

        
        grid.move_runner(self.rect, self.x, self.y)
        canv.pack()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0

        self.path_length = 0

        self.rect = canv.create_rectangle(WIN_WITDH / GRID_WIDTH * self.x, WIN_HEIGHT / GRID_HEIGHT * self.y , WIN_WITDH / GRID_WIDTH * self.x + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * self.y + WIN_HEIGHT / GRID_HEIGHT, fill="lime")

    def change_dir(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def move(self):
        nx = self.x + self.dx
        ny = self.y + self.dy

        if (nx >= 0 and nx < GRID_WIDTH and ny >= 0 and ny < GRID_HEIGHT):
            self.x += self.dx
            self.y += self.dy

        if (grid.get_cube(self.x, self.y) == 0):
            grid.setPath(self.x, self.y)
            self.path_length += 1
        elif (self.path_length > 0):
            grid.fill()
            self.path_length = 0



        canv.coords(self.rect, WIN_WITDH / GRID_WIDTH * self.x, WIN_HEIGHT / GRID_HEIGHT * self.y , WIN_WITDH / GRID_WIDTH * self.x + WIN_WITDH / GRID_WIDTH, WIN_HEIGHT / GRID_HEIGHT * self.y + WIN_HEIGHT / GRID_HEIGHT)

        canv.pack()


grid = Grid1(GRID_WIDTH, GRID_HEIGHT)
Runner.set_grid(grid)

runners = []
for i in range(3):
    runners.append(Runner())


player = Player(0, 0)

def update():

    for i in range(len(runners)):
        runners[i].move()
    player.move()
    master.after(200, update)
    



master.bind("<Left>", lambda x : player.change_dir(-1, 0))
master.bind("<Right>", lambda x: player.change_dir(1, 0))
master.bind("<Up>", lambda x: player.change_dir(0, -1))
master.bind("<Down>", lambda x: player.change_dir(0, 1))
master.bind("<space>", lambda x: player.change_dir(0, 0))
update()



mainloop()