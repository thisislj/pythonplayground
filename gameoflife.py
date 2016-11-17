#!/bin/env python

import argparse
import sys
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def get_args():
    argparser = argparse.ArgumentParser(description="Conway's life game")

    # configuration of src and target workspaces
    argparser.add_argument('--size-grid', required=True, 
                           help='size of grid')
    argparser.add_argument('--use-glider', action='store_true',
                           help='use glider or not')

    return argparser.parse_args()

def add_glider(tgt, off_x, off_y):
    glider = np.array([0, 0, 1,
                       1, 0, 1,
                       0, 1, 1])
    glider = glider.reshape(3,3)
    tgt[off_x:off_x+3,off_y:off_y+3] = glider
    

def cell_survived(grid, off_x, off_y):
    w, h = grid.shape
    cell_alive = grid[(off_x)%w, (off_y)%h]
    sum = -cell_alive

    for x in range(off_x-1, off_x+2):
        for y in range(off_y-1, off_y+2):
            sum += grid[x%w, y%w]

    if cell_alive:
        if sum < 2 or sum > 3:
            return 0
    else:
        if sum == 3:
            return 1

    return cell_alive


def update(frameNum, img, grid):
    new_grid = np.zeros(grid.size).reshape(grid.shape)
    w, h = grid.shape

    for x in range(w):
        for y in range(h):
            new_grid[x, y] = cell_survived(grid, x, y)

    img.set_data(new_grid)
    grid[:] = new_grid[:]

if __name__ == '__main__':
    args = get_args()
    print args.size_grid
    print args.use_glider

    size_grid = int(args.size_grid)

    world = np.random.choice([0, 1], size_grid**2, p=[0.5, 0.5])
    world = world.reshape(size_grid, size_grid)

    if args.use_glider:
        world = np.zeros(size_grid*size_grid)
        world = world.reshape(size_grid, size_grid)
        add_glider(world, 1, 1)
        add_glider(world, 10, 10)
        add_glider(world, 15, 15)


    #img = plt.imshow(world, interpolation='nearest')
    #plt.show()

    fig, ax = plt.subplots()
    img = ax.imshow(world, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, world),
                                  frames=200,
                                  interval=50,
                                  save_count=5)

    plt.show()
