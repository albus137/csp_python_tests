#!/usr/bin/env python3

from constraint import *
from pprint import pprint

# grid definition
grid = [[5, 3, 0,  0, 7, 0,  0, 0, 0],
        [6, 0, 0,  1, 9, 5,  0, 0, 0],
        [0, 9, 8,  0, 0, 0,  0, 6, 0],
        
        [8, 0, 0,  0, 6, 0,  0, 0, 3],
        [4, 0, 0,  8, 0, 3,  0, 0, 1],
        [7, 0, 0,  0, 2, 0,  0, 0, 6],
        
        [0, 6, 0,  0, 0, 0,  2, 8, 0],
        [0, 0, 0,  4, 1, 9,  0, 0, 5],
        [0, 0, 0,  0, 8, 0,  0, 7, 9]]
n_lines, n_cols = 9, 9
n_squares, size_square = 3, 3

# coordinates grid definition (grid_coor[i][j] is equal to tuple (i, j))
grid_coor = [[(i, j) for j in range(n_cols)] for i in range(n_lines)]

# problem definition
problem = Problem()

# variables definition
for i in range(n_lines):
    for j in range(n_cols):
        if grid[i][j] == 0:
            domain = range(1, 10)
        else:
            domain = [grid[i][j]]

        problem.addVariable(grid_coor[i][j], domain)

# constraints on lines
for i in range(n_lines):
    coors = [(i, j) for j in range(n_cols)]
    problem.addConstraint(AllDifferentConstraint(), coors)

# constraints on columns
for j in range(n_cols):
    coors = [(i, j) for i in range(n_lines)]
    problem.addConstraint(AllDifferentConstraint(), coors)

# constraints on 3 by 3 squares
for I in range(n_squares):
    for J in range(n_squares):
        coors = [(i, j) for j in range(J*size_square, (J+1)*size_square)
                 for i in range(I*size_square, (I+1)*size_square)]
        problem.addConstraint(AllDifferentConstraint(), coors)

# problem solving
solution = problem.getSolution()

if solution is None:
    print('there is no solution')
else:
    # fill the grid with the values found
    for coor in solution:
        grid[coor[0]][coor[1]] = solution[coor] 

    # display the grid
    pprint(grid)
