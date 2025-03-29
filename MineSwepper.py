import turtle
import random
import time
import winsound

def count_mines_around(x, y):
    #this funtion will count the number of mines surrounding a given cell in a 2d grid.
    #x, y represent coordinates of the central cell.
    global c
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        if 0 <= x + dx < dimension and 0 <= y + dy < dimension and m2[x + dx][y + dy] == 1:
            c += 1

def reveal_square(x, y):
    #this funtion reveal the cell you click on, x and y represent the coord of the cell to be revealed.
    global m2, c, dimension, m3
    c = 0
    if m3[x][y] == -1 and 0 <= x < dimension and 0 <= y < dimension:
        count_mines_around(x, y)
        m3[x][y] = c
        gridSquare.goto(coordinates[x][y])
        gridSquare.setheading(-180)
        gridSquare.color("white")
        gridSquare.pencolor("black")
        gridSquare.stamp()
        if c == 0:
            reveal_adjacent_squares(x, y)
        else:
            gridSquare.write(c)

def reveal_adjacent_squares(x, y):
    #The funtion reveal all the cell adcent to a given cell
    #funtion iterates over a list of tuples representing the 8 possible directions around the central cell.
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        reveal_square_if_valid(x + dx, y + dy)

def reveal_square_if_valid(x, y):
    #this funtion is to ensure that a cell is revealed only if its coord are within the valid bounds of the grid
    #x y represnt the corrd of cell to be revealed
    if 0 <= x < dimension and 0 <= y < dimension:
        reveal_square(x, y)

def get_square_coordinates(x,y):
    indexX = 100000
    indexY = 100000
    dist = 100000000
    for row in range(len(coordinates)):
        for col in range(len(coordinates[row])):
            currX = coordinates[row][col][0]
            currY = coordinates[row][col][1]
            currDist = ((x - currX )**2 + (y -currY )**2) ** 0.5
            if currDist < dist:
                dist = currDist
                indexX = col
                indexY = row
    return indexY, indexX

def left_click(x, y):
    #the funtion handles left clicks on a cell
    #x and y represent the screen coord of the click.
    #also when you lose, it exit the game after 3 seconds.
    global m3
    row, col = get_square_coordinates(x, y)
    gridSquare.goto(coordinates[row][col])
    gridSquare.showturtle()
    if m2[row][col] == 1:
    #    winsound.PlaySound("C:\\Users\\andyl\\OneDrive\\Documents\\pythonProjects\\pythonFiles\\bumbpop.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
        myWin.bgcolor("red")
        time.sleep(3)
    #    winsound.PlaySound("C:\\Users\\andyl\\OneDrive\\Documents\\pythonProjects\\pythonFiles\\looser.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
        print("LOOSER!")
        gridSquare.clear()
        gridSquare.goto(-50, 0)
        gridSquare.write("LOOSER!", font=("Arial", 20, "normal"))
        time.sleep(5)
        myWin.bye()
        return
    if m1[row][col] == 0:
        gridSquare.fillcolor("white")
        m1[row][col] = 1
        reveal_square(row, col)
        gridSquare.hideturtle()
        myWin.update()
    check_win()

def right_click(x, y):
    #this funtion handles the right clicks on a cell.
    global f
    row, col = get_square_coordinates(x, y)
    if m3[row][col] == -1:
        gridSquare.goto(coordinates[row][col])
        gridSquare.showturtle()
        if m1[row][col] == 0:
            gridSquare.fillcolor("red")
            m1[row][col] = 2
            f += 1
        elif m1[row][col] == 2:
            gridSquare.fillcolor("#000080")
            m1[row][col] = 0
            f -= 1
        gridSquare.stamp()
        gridSquare.hideturtle()
    myWin.update()
    check_win()

def check_win():
    #determin if the player has won, 
    global m3, dimension, mine
    mine = sum(row.count(-1) for row in m3)
    if mine == M:
    #    winsound.PlaySound("C:\\Users\\andyl\\OneDrive\\Documents\\pythonProjects\\pythonFiles\\Win.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
        print("You Win!!")
        gridSquare.clear()
        gridSquare.goto(-50, 0)
        gridSquare.write("You Win!", font=("Arial", 20, "normal"))
        time.sleep(5)
        myWin.bye()

def show_grid_coords():
    #used for debugging, no need now.
    for row in coordinates:
        print(row)

def use_map():
    #visually update the game grid, it use gridSquare to draw the grid and myWin.update to update.
    gridSquare.showturtle()
    for row in range(len(m1)):
        for col in range(len(m1[row])):
            if m1[row][col] == 0:
                gridSquare.fillcolor("#000080")
            elif m1[row][col] == 2:
                gridSquare.fillcolor("red")
            gridSquare.goto(coordinates[row][col])
            gridSquare.stamp()
    gridSquare.hideturtle()
    myWin.update()

def create_grid(screen_size, half_screen, sq_size, gutter, offset, dimension):
    #create and visually render a  grid for the game.
    global coordinates
    start_x = int(-1 * half_screen + sq_size / 2 + gutter + offset)
    start_y = int(half_screen - sq_size / 2 - gutter - offset)
    gridSquare.goto(start_x, start_y)
    end_x = start_x + dimension * sq_size
    end_y = start_y - dimension * sq_size
    for y in range(start_y, end_y, -sq_size):
        row = []
        for x in range(start_x, end_x, sq_size):
            gridSquare.goto(x, y)
            gridSquare.stamp()
            row.append((x, y))
        coordinates.append(row)
    myWin.update()

#----------------------------------window and grid parameters-------------------------
screenSize = 700
dimension = 20
gutter = 30
offset = -3
halfScreen = screenSize // 2
usableSpace = screenSize - 2 * gutter
sqSize = usableSpace // dimension
turtSize = sqSize / 20

#-------------------------------------window and turtle creation-------------------
mine = 0
f = 0
turtle.setup(screenSize, screenSize)
myWin = turtle.Screen()
myWin.title("MineSwepper")
gridSquare = turtle.Turtle()
gridSquare.penup()
gridSquare.speed(0)

#----draw border
gridSquare.goto(-halfScreen, halfScreen)
gridSquare.pendown()
for i in range(4):
    gridSquare.forward(screenSize)
    gridSquare.right(90)
gridSquare.penup()
gridSquare.goto(0, 0)
gridSquare.turtlesize(turtSize, turtSize)
gridSquare.shape("square")
gridSquare.color("white")
gridSquare.pencolor("black")

#---border drawn
count = turtle.Turtle()
count.penup()
count.speed(0)
count.shape("square")
count.color("white")
count.pencolor("black")
count.hideturtle()
count.goto(30 - screenSize / 2, screenSize / 2 - 30)

#------------------------------------draw the grid and store the coordinates
coordinates = []
myWin.tracer(0, 0)
create_grid(screenSize, halfScreen, sqSize, gutter, offset, dimension)

#-------------------------initialize map data --------------
M = 0
#m1 is a 2d array, each element is initualized to 0. m1 contain dimention number of inner lists
m1 = []
for _ in range(dimension):
    m1.append([0] * dimension)
#m2 is similar to m1, each element is initialized to 0, structure are identical to m1
m2 = []
for _ in range(dimension):
    m2.append([0] * dimension)
#m3, each element is intialized to -1
m3 = []
for _ in range(dimension):
    m3.append([-1] * dimension)
use_map()

for _ in range((dimension ** 2) // 7):
    while True:
        x, y = random.randint(0, dimension - 1), random.randint(0, dimension - 1)
        if m2[x][y] == 0:
            m2[x][y] = 1
            M += 1
            break

myWin.listen()
myWin.onclick(left_click)
#btn 1 rep lmb, btn 2 rep mmb, btn 3 rep rmb
myWin.onclick(right_click, btn=3)
myWin.mainloop()