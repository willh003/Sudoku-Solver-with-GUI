import pygame, sys, time
from pygame.locals import *
import solver

window_size = 108  # Divisible by 9, making sure all grid spaces are equal
window_multiplier = 5 # Modify this to change size of window 

window_width = window_size * window_multiplier
window_height = window_size * window_multiplier

square_size = (window_width) // 3
cell_size = (window_width) // 9

white = (255, 255, 255)
black = (0, 0, 0)
light_gray = (200, 200, 200)
blue = (20, 20, 250)
green = (20, 255, 20)

fps = 15

board_init = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]

def drawGrid(): # Draws sudoku grid
    # Small boxes
    for x in range(0, window_width, cell_size): 
        pygame.draw.line(displaysurf, light_gray, (x, 0),(x, window_height))
    for y in range (0, window_height, cell_size): 
        pygame.draw.line(displaysurf, light_gray, (0,y), (window_width, y))
    # Big boxes
    for x in range(0, window_width, square_size): 
        pygame.draw.line(displaysurf, black, (x,0),(x, window_height))
    for y in range (0, window_height, square_size):
        pygame.draw.line(displaysurf, black, (0,y), (window_width, y))
    return None

def makeDict(): # Makes dictionary for grid where key = grid line (row or col number) and value = coordinate
    key_list = []
    grid_dict = {}
    for i in range(1, 10):
        key_list.append([i])
        key_list[i - 1].append(cell_size * (i - 1))
    for j in key_list:
        grid_dict[j[0]] = j[1]
    return grid_dict

def drawBox(mousex, mousey, color): # Draws blue box around cursor
    boxx = ((mousex*9) // window_width) * (cell_size)
    boxy = ((mousey*9) // window_height) * (cell_size)
    pygame.draw.rect(displaysurf, color, (boxx, boxy, cell_size, cell_size), 1)

def delCell(mousex, mousey):
    screenx = ((mousex*9) // window_width) * (cell_size)
    screeny = ((mousey*9) // window_height) * (cell_size)
    displaysurf.fill(white, (screenx, screeny, cell_size, cell_size))

def writeNumber(mousex, mousey, num): # Creates the grid coords from mouse locations, displays number
    grid_dict_init = makeDict()
    gridx = ((mousex*9) // window_width) + 1
    gridy = ((mousey*9) // window_height) + 1
    num_msg = basicfont.render('%s' %(num), True, black)
    displaysurf.blit(num_msg, [int(grid_dict_init[gridx] + (cell_size / 4)), int(grid_dict_init[gridy] + (cell_size / 4)) ]) # grid_dict[gridx]: coordinate value of text in box from grid coordinate

    # Add user input to list compatible with solver
    global board_init
    board_init[gridy - 1][gridx - 1] = num
    
def getSolutions(): # Find way to format board as list compatible with solver (from user input) and then back to GUI
    error_msg = basicfont.render('Error: unsolvable board', True, black)
    try:
        solver.solve(board_init)
        return(board_init)
    except:
        displaysurf.fill(white)
        displaysurf.blit(error_msg)

def showSolutions():
    grid_dict_fin = makeDict()
    solved_board = getSolutions()
    for j in range(9):  # PROBLEM: you need for 'j in solved_board' to access i, but j is a list, not an integer index
        for i in range(9):
            num = solved_board[j][i]  
            num_dis = basicfont.render('%s' %(num), True, black)
            displaysurf.blit(num_dis, [int(grid_dict_fin[i + 1] + (cell_size / 4)), int(grid_dict_fin[j + 1] + (cell_size / 4)) ])

def main(): # Main function
    global fpsclock, displaysurf
    pygame.init()
    fpsclock = pygame.time.Clock()
    displaysurf = pygame.display.set_mode((window_width, window_height))

    mouse_clicked = False
    mousex = 0
    mousey = 0

    pygame.display.set_caption('Sodoku Solver') 

    global basicfont, basicfontsize
    basicfontsize = 45
    basicfont = pygame.font.Font('freesansbold.ttf', basicfontsize)

    displaysurf.fill(white)
    drawGrid()

    num_input = None
    game_solve = False
    while not game_solve: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
               
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_solve = True
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

            if mouse_clicked:
                xmouse, ymouse = pygame.mouse.get_pos()
                drawBox(xmouse, ymouse, green)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        num_input = 1
                    if event.key == pygame.K_2:
                        num_input = 2
                    if event.key == pygame.K_3:
                        num_input = 3
                    if event.key == pygame.K_4:
                        num_input = 4
                    if event.key == pygame.K_5:
                        num_input = 5
                    if event.key == pygame.K_6:
                        num_input = 6
                    if event.key == pygame.K_7:
                        num_input = 7
                    if event.key == pygame.K_8:
                        num_input = 8
                    if event.key == pygame.K_9:
                        num_input = 9
                    if event.key == pygame.K_DELETE:
                        writeNumber(xmouse, ymouse, 0) # Replaces number in list with 0
                        delCell(xmouse, ymouse) # Deletes Cell Graphic
                    if num_input != None:
                        writeNumber(xmouse, ymouse, num_input)
                    num_input = None
                    mouse_clicked = False

        drawGrid()    
        pygame.display.update()   
        fpsclock.tick(fps * 5)

    while game_solve:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board_init = [
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0]
                    ]
                    game_solve = False       
        displaysurf.fill(white)
        drawGrid()
        showSolutions()
        pygame.display.update()

if __name__ == '__main__':
    main()
