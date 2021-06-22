"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]
def readConfig(path):
    file=open(path,"r")
    x=0
    y=0
    lines=file.readlines()
    N=len(lines)
    grid = np.array([])
    grid = np.zeros((N*N), dtype=int).reshape(N, N)
    for line in lines:
        y=0
        for char in line:
            if char!=' ' and char !='\n':
                grid[x][y]=int(char)*ON
                y+=1
        x+=1
    file.close()
    return grid,N
def checkNeighbor(grid,i,j):
    sum=0
    for x in range(-1,2):
        for y in range(-1,2):
            try:
                sum+=grid[i+x][j+y]
            except:
                pass
    sum-=grid[i][j]
    return sum/ON
def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    # TODO: Implement the rules of Conway's Game of Life
    for x in range(0,N):
        for y in range(0,N):
            current=grid[x][y]
            validation=checkNeighbor(grid,x,y)
            if(current==255 and (2<=validation<=3)):
                current=255
            elif(current==0 and validation==3):
                current=255
            else:
                current=0
            newGrid[x][y]=current
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    
    # set check if config is passed as command line parameter
    if len(sys.argv)>1:
        # declare grid
        grid,N=readConfig(sys.argv[1])
    else:
        N = int(input("introduce size of the universe"))
        # declare grid
        grid = np.array([])
        # populate grid with random on/off - more off than on
        grid = randomGrid(N)
        # Uncomment lines to see the "glider" demo
        #grid = np.zeros(N*N).reshape(N, N)
        #addGlider(1, 1, grid)
        
    # set animation update interval
    updateInterval = 200

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
    main()