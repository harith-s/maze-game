import numpy as np
import pygame

def check_repetition(point, solver_visited):
    for distance_list in solver_visited:
        for isodistance_point in distance_list:
            if point == isodistance_point:
                return False
    return True
            
def check_adj(point, l, solution, place_holder):
    i = point[0]
    j = point[1]
    if (i,j-1) in l and place_holder[point][-1] == "0": 
        solution.insert(0, 'r')
        return (i,j-1)
    elif (i,j+1) in l and place_holder[point][-2] == "0": 
        solution.insert(0,'l')
        return (i,j+1)
    elif (i+1, j) in l and place_holder[point][-3] == "0":  
        solution.insert(0, 'u')
        return (i+1,j)
    elif (i-1, j) in l and place_holder[point][-4] == "0": 
        solution.insert(0,'d')
        return (i-1,j)

    
def solver(place_holder,rows,columns, file_path):
    f = open(file_path, 'w')
    solver_visited = []
    solver_visited.append([(0,0)])
    end = (rows - 1, columns - 1)
    while check_repetition(end, solver_visited):
        poss_neighbors = set()
        for cell in solver_visited[-1]:
    
            i = cell[0] 
            j = cell[1] 
            value = place_holder[i,j]
            
            if i < rows - 1 and value[-3] == "0" and check_repetition((i+1,j),solver_visited): poss_neighbors.add((i+1,j))
            if i > 0 and value[-4] == "0" and check_repetition((i-1,j),solver_visited): poss_neighbors.add((i-1,j))
            if j < columns - 1 and value[-2] == "0" and check_repetition((i,j+1),solver_visited): poss_neighbors.add((i,j+1))
            if j > 0 and value[-1] == "0" and check_repetition((i,j-1),solver_visited): poss_neighbors.add((i,j-1))
        solver_visited.append(list(poss_neighbors))
    solution = []
    index = -2

    point = end
    while point != (0,0):
        point = check_adj(point, solver_visited[index], solution, place_holder)
        index = index - 1
    f.write(str(solution))



