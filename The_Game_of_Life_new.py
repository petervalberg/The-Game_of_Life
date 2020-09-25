'''
Written by Peter Valberg 2018.
A simulation of "The Game of Life".
Invented by John H. Conway in 1970.

Rules:
1. Any live cell with fewer than two live neighbors dies.
2. Any live cell with two or three live neighbors lives on.
3. Any live cell with more than three live neighbors dies.
4. Any dead cell with exactly three live neighbors comes alive.
'''

from tkinter import *
import random, time


# definitions for colors and fonts
font1 = ('Helvetica', 12, 'bold', 'roman')
font2 = ('Helvetica', 10, 'bold', 'roman')
neutral_color = 'SystemButtonFace'
active_color = 'black'
button_color = 'lightgray'
active_button_color = 'snow3'

# definitions for sizes etc.
x, y = 0, 1
guiSize = '1445x900'
guiStartPosition = '+150+50'
canvasSize = [1400, 800]
cellSize = [20, 20]
columns, rows = [int(canvasSize[x]/cellSize[x]), int(canvasSize[y]/cellSize[y])]

# other definitions
delay = 150  # that's in milliseconds
currentGeneration = []
nextGeneration = []
generationNumber = 0
pauseCounter = 0   # used to control run/pause
paused = False   # used to control run/stop
infoText =['', 'Game is paused, press "Pause/Run" to continue.','Press "New" to start.']
    
def build_currentGeneration():
    # build array-like list for current generation (filled with zeros)
    global currentGeneration
    for r in range(0, rows):
        currentGeneration.insert(r, [0]*columns)

def build_nextGeneration():
    # build array-like list for next generation (filled with zeros)
    global nextGeneration
    for r in range(0, rows):
        nextGeneration.insert(r, [0]*columns)

def dataTransfer():
    # transfer nextGeneration to currentGeneration
    global currentGeneration, nextGeneration
    for r in range(0, rows):
        for c in range(0, columns):
            currentGeneration[r][c] = nextGeneration[r][c]
    root.update_idletasks()

def calculateNextGeneration():
    # calculate nextGeneration according to rules
    global currentGeneration, nextGeneration
    for r in range(0, rows):
        for c in range(0, columns):
            # calculate the sum of the eight neighbour-cells (wrapped around the edges)
            # left and right edges of the field are considered to neighbours,
            # and the top and bottom edges are also considered to neighbours.
            sum_ = 0
            sum_ += currentGeneration[(r-1) % rows][(c-1) % columns]
            sum_ += currentGeneration[(r-1) % rows][c]
            sum_ += currentGeneration[(r-1) % rows][(c+1) % columns]
            sum_ += currentGeneration[r][(c-1) % columns]
            sum_ += currentGeneration[r][(c+1) % columns]
            sum_ += currentGeneration[(r+1) % rows][(c-1) % columns]
            sum_ += currentGeneration[(r+1) % rows][c]
            sum_ += currentGeneration[(r+1) % rows][(c+1) % columns]
            
            # determine if a current cell is alive/dead in nextGeneration
            # and write the data to nextGeneration
            if currentGeneration[r][c] == 1 and sum_ < 2:
                nextGeneration[r][c] = 0
            elif currentGeneration[r][c] == 1 and (sum_ == 2 or sum_ == 3):
                nextGeneration[r][c] = 1
            elif currentGeneration[r][c] == 1 and sum_ > 3:
                nextGeneration[r][c] = 0
            elif currentGeneration[r][c] == 0 and sum_ == 3:
                nextGeneration[r][c] = 1
            else:
                pass
    root.update_idletasks()

def firstGeneration():
    # calculate first current generation randomly
    global currentGeneration
    for r in range(0, rows):
        for c in range(0, columns):
            currentGeneration[r][c] = random.choice([0, 1])

def drawCurrentGeneration():
    # draw currentGeneration on the canvas
    globals()['generationNumber'] += 1   # counter for generations
    canvas.delete(ALL)
    for r in range(0, rows):
        for c in range(0, columns):
            if currentGeneration[r][c] == 1:
                canvas.create_rectangle(c*cellSize[x], r*cellSize[y], (c+1)*(cellSize[x]), (r+1)*(cellSize[y]), fill=active_color, outline=active_color, width=1)
            else:
                canvas.create_rectangle(c*cellSize[x], r*cellSize[y], (c+1)*(cellSize[x]), (r+1)*(cellSize[y]), fill=neutral_color, outline=neutral_color, width=1)
    root.after(delay, calculateNextGeneration())
    root.update_idletasks()

def gameloop():
    # a sort of mainloop
    root.update_idletasks()
    calculateNextGeneration()
    dataTransfer()
    if paused == False:
        # contiune to run program
        generation.config(text=generationNumber)   # update generation count
        drawCurrentGeneration()
        root.after(delay, gameloop)

# buttonfunctions
def new_pushed():
    # generates a new population and draw canvas
    globals()['generationNumber'] = 0   # reset counter (generations)
    globals()['pauseCounter'] = 0   # reset pauseCounter
    globals()['paused'] = False
    infoLabel.config(text=infoText[0])
    firstGeneration()
    drawCurrentGeneration()
    gameloop()

def pause():
    # pause/run program
    globals()['pauseCounter'] += 1
    if pauseCounter % 2 != 0:
        # pause program
        globals()['paused'] = True
        infoLabel.config(text=infoText[1])
    else:
        # run program
        globals()['paused'] = False
        infoLabel.config(text=infoText[0])
        gameloop()

def exit_():
    # ends the program
    root.destroy()

# GUI definitions
root = Tk()
root.title("Conway's Game of Life")
root.iconbitmap("life.ico")  # modify program-icon here
root.geometry(guiSize)
root.geometry(guiStartPosition)
root.resizable(width=False, height=False)
root.configure(bg=neutral_color)

# frames, buttons, canvas etc.
topframe = Frame(root, bg=neutral_color)
topframe.config(borderwidth=2, relief=RIDGE)
Button(topframe, text='New', font=font1, bg=button_color, activebackground=active_button_color, width=10, command=lambda:new_pushed()).pack(side=LEFT, expand=0)
Button(topframe, text='Pause/Run', font=font1, bg=button_color, activebackground=active_button_color, width=10, command=lambda:pause()).pack(side=LEFT, expand=0)
Button(topframe, text='Exit', font=font1, bg=button_color, activebackground=active_button_color, width=10, command=lambda:exit_()).pack(side=LEFT, expand=0)
Label(topframe, text=None, bg=neutral_color, width=10).pack(side=LEFT, expand=0)
Label(topframe, text='Generation:', bg=neutral_color, fg='black', font=font1, width=10, justify=RIGHT).pack(side=LEFT, expand=0)
generation = Label(topframe, text='0', bg=neutral_color, fg='black', font=font1, width=10, justify=LEFT)
generation.pack(side=LEFT, expand=0)
infoLabel = Label(topframe, text='', bg=neutral_color, fg='red', font=font1, justify=LEFT)
infoLabel.pack(side=LEFT, expand=1)
topframe.pack(padx=10, pady=10, fill=BOTH)

canvas = Canvas(root, width=canvasSize[x], height=canvasSize[y], bg=neutral_color, bd=1, relief=RIDGE)
canvas.pack()

bottomframe = Frame(root, bg=neutral_color)
Label(bottomframe, text='Version 2.0', bg=neutral_color, fg='gray', font=font2).pack(side=LEFT, expand=0)
Label(bottomframe, text='Peter Valberg 2018', bg=neutral_color, fg='gray', font=font2).pack(side=RIGHT, expand=0)
bottomframe.pack(padx=10, pady=10, fill=BOTH)

# create array-like lists for current and next generation
build_currentGeneration()
build_nextGeneration()
infoLabel.config(text=infoText[2])

root.mainloop()
