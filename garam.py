#!/usr/bin/env python3

from constraint import *
import pyexcel as pe
from time import time

# create the problem object
problem = Problem(RecursiveBacktrackingSolver())

# import the Garam grid
grid = pe.get_array(file_name='csp_grid.ods')
n_lines, n_cols = len(grid), len(grid[0])

# display the Garam grid nicely
print('Initial grid:')
print()
for i in range(n_lines):
    for j in range(n_cols):
        if grid[i][j] == '':
            print(' ', end='')
        else:
            print(grid[i][j], end='')
    print()

# add the variables to the problem
for i in range(n_lines):
    for j in range(n_cols):
        if grid[i][j] == '?':
            domain = range(0, 10)
        elif type(grid[i][j]) == int:
            domain = [grid[i][j]]

        problem.addVariable((i, j), domain)

# create the "coor grid" (grid whose cases are tuples containing the cases coordinates)
grid_coor = [[(i, j) for j in range(n_cols)] for i in range(n_lines)]

# set the first case of each constraint
h_constraints_origins = [[0, 0], [0, 8],
                         [2, 4],
                         [5, 0], [5, 8],
                         [9, 0], [9, 8],
                         [11, 4],
                         [14, 0], [14, 8]]

v_constraints_origins = [[0, 0], [9, 0],
                         [5, 2],
                         [0, 4], [9, 4],
                         [0, 8], [9, 8],
                         [5, 10],
                         [0, 12], [9, 12]]

# get the horizontal constraints
h_constraints = []
for origin in h_constraints_origins:
    i_origin, j_origin = origin
    constraint = grid_coor[i_origin][j_origin:j_origin+5]
    h_constraints.append(constraint)

# get the vertical constraints
v_constraints = []
for k in range(len(v_constraints_origins)):
    i_origin, j_origin = v_constraints_origins[k]

    if k == 2 or k == 7:
        nb_cases = 5
    else:
        nb_cases = 6

    constraint = [line[j_origin] for line in grid_coor[i_origin:i_origin+nb_cases]]
    v_constraints.append(constraint)

# add the constraints to the problem
constraints = h_constraints + v_constraints

for constraint in constraints:
    # get the operation type (+, - or *)
    i, j = constraint[1]
    op = grid[i][j]

    if len(constraint) == 5:
        if op == '+':
            constraint_function = lambda a, b, c: a+b == c
        elif op == '-':
            constraint_function = lambda a, b, c: a-b == c
        elif op == '*':
            constraint_function = lambda a, b, c: a*b == c

        problem.addConstraint(constraint_function, (constraint[0], constraint[2], constraint[4]))

        print('{}{}{}={}'.format(grid[constraint[0][0]][constraint[0][1]],
                                 op,
                                 grid[constraint[2][0]][constraint[2][1]],
                                 grid[constraint[4][0]][constraint[4][1]]))
    elif len(constraint) == 6:
        if op == '+':
            constraint_function = lambda a, b, c, d: a+b == c*10+d
        elif op == '-':
            constraint_function = lambda a, b, c, d: a-b == c*10+d
        elif op == '*':
            constraint_function = lambda a, b, c, d: a*b == c*10+d

        problem.addConstraint(constraint_function, (constraint[0], constraint[2], constraint[4], constraint[5]))

        print('{}{}{}={}{}'.format(grid[constraint[0][0]][constraint[0][1]],
                                   op,
                                   grid[constraint[2][0]][constraint[2][1]],
                                   grid[constraint[4][0]][constraint[4][1]],
                                   grid[constraint[5][0]][constraint[5][1]]))

print()
print('Solving the problem...')

# solve the problem
start = time()
solution = problem.getSolution()
end = time()
print('Elapsed time: {:.0f} s'.format(end-start))

# display the solution
print()
print('Solved grid:')
print()
for i in range(n_lines):
    for j in range(n_cols):
        if grid[i][j] == '?' or type(grid[i][j]) == int:
            print(solution[(i, j)], end='')
        elif grid[i][j] == '':
            print(' ', end='')
        elif type(grid[i][j]) == str:
            print(grid[i][j], end='')
    print()
