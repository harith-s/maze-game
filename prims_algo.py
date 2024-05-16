import numpy as np
import pygame
import random
import time
import game_screen
#import path_finder
#from player import Player

pygame.init()
screen = pygame.display.set_mode((800, 600))

# prims algorithm

def prims_algo_random(array, visited):
    rows,columns = np.shape(array)
    while len(visited) != rows*columns:
            neighbours  = []
            for cell in visited:
                i = cell[0] 
                j = cell[1] 
                if i < rows - 1: neighbours.append((i+1,j))
                if i > 0: neighbours.append((i-1,j))
                if j < columns - 1: neighbours.append((i,j+1))
                if j > 0: neighbours.append((i,j-1))
            poss_neighbours = list(neighbours)
            for i in neighbours:
                if i in visited:
                    poss_neighbours.remove(i)

            cell = poss_neighbours[np.random.choice(list(range(len(poss_neighbours))))]
            i = cell[0] 
            j = cell[1] 
            neighbour_cell = [(i,j-1),(i,j+1),(i+1,j),(i-1,j)]
            neighbour_cell_list = [cell for cell in neighbour_cell if cell in visited]

            neighbour_cell = neighbour_cell_list[np.random.choice(list(range(len(neighbour_cell_list))))]
            if neighbour_cell == (i,j-1):
                array[i,j-1] -= 2
                array[i,j] -= 1
            elif neighbour_cell == (i, j+1):
                array[i,j+1] -= 1
                array[i,j] -= 2
            elif neighbour_cell == (i+1, j):
                array[i+1, j] -= 8
                array[i,j] -= 4
            elif neighbour_cell == (i-1,j):
                array[i-1, j] -= 4
                array[i,j] -= 8

            visited.append(cell)

    maze = np.zeros_like(array).astype(str)
    for idx, x in np.ndenumerate(array):
        maze[idx] = bin(int(x))[2:].zfill(5)
    display_array = np.pad(array, 1, mode="constant", constant_values=31)
    display_maze  = np.zeros_like(display_array).astype(str)
    for idx, x in np.ndenumerate(display_array):
        display_maze[idx] = bin(int(x))[2:].zfill(5)
    return maze, display_maze

# code for adding walls according to the array


def prims_algo_notrandom(array, visited):
    rows, columns = np.shape(array)
    weights = generate_weights(rows, columns)
    # print("weights: ",weights)
    maze  = np.zeros_like(array).astype(str)
    for idx, x in np.ndenumerate(array):
        maze[idx] = bin(int(x))[2:].zfill(4)
    while len(visited) != rows*columns:
            # print("Visiting cell: ",visited)
            neighbours  = []
            for cell in visited:
                i = cell[0] 
                j = cell[1] 
                if i < rows - 1 and (i+1, j) not in neighbours:
                    neighbours.append((i+1, j))
                if i > 0 and (i-i,j) not in neighbours: 
                    neighbours.append((i-1,j))
                if j < columns - 1 and (i,j+1) not in neighbours: 
                    neighbours.append((i,j+1))
                if j > 0 and (i,j-1) not in neighbours: 
                    neighbours.append((i,j-1))
            poss_neighbours = list(neighbours)
            for i in neighbours:
                if i in visited:
                    poss_neighbours.remove(i)
            # print("Possible neighbours after removing visted cells: ",poss_neighbours)

            # now I have to choose the edges which come under the maximum weight
            max_weight = "0"
            for index in visited:
                value = weights[index]
                for char in value:
                    if char > max_weight:
                        max_weight = char
            
            
            choice = []
            chosen_visited_cells = []
            while not(choice):
                for idx in visited:
                    i,j = idx
                    cell_chosen = idx
                    value = weights[idx]
                    if value[0] == max_weight and (i-1,j) in poss_neighbours: 
                        choice.append((i-1,j))
                        chosen_visited_cells.append((i,j))

                    if value[1] == max_weight and (i+1,j) in poss_neighbours:
                        choice.append((i+1,j))
                        chosen_visited_cells.append((i,j))
                    if value[2] ==  max_weight and (i,j+1) in poss_neighbours: 
                        choice.append((i,j+1))
                        chosen_visited_cells.append((i,j))
                    if value[3] == max_weight and (i,j-1) in poss_neighbours: 
                        choice.append((i,j-1)) 
                        chosen_visited_cells.append((i,j))
                # print(choice)
                max_weight = str(int(max_weight) - 1)
            # print(max_weight)
            # print(weights)
            # print(choice)
            
            random_index = np.random.choice(len(choice))    
            cell = choice[random_index]
            visited_cell = chosen_visited_cells[random_index]

            i = cell[0] 
            j = cell[1] 
            # print(weights[i,j])
            if visited_cell == (i,j-1):
                array[i,j-1] -= 2
                array[i,j] -= 1
                weights[i,j] = weights[i,j][0] + weights[i,j][1] + weights[i,j][2] + '0'
                weights[i,j-1] = weights[i,j-1][0] + weights[i,j-1][1] + '0' + weights[i,j-1][3]
            elif visited_cell == (i, j+1):
                array[i,j+1] -= 1
                array[i,j] -= 2
                weights[i,j] = weights[i,j][0] + weights[i,j][1] + "0" + weights[i,j][3]
                weights[i,j+1] = weights[i,j+1][0] + weights[i,j+1][1] + weights[i,j+1][2] + "0"
            elif visited_cell == (i+1, j):
                array[i+1, j] -= 8
                array[i,j] -= 4
                weights[i,j] = weights[i,j][0] + '0' + weights[i,j][2:]
                weights[i+1,j] = '0' + weights[i+1,j][1:]
            elif visited_cell == (i-1,j):
                array[i-1, j] -= 4
                array[i,j] -= 8
                weights[i,j] = '0' + weights[i,j][1:]
                weights[i-1,j] = weights[i-1,j][0] + '0' + weights[i-1,j][2:]

            visited.append(cell)
    maze = np.zeros_like(array).astype(str)
    for idx, x in np.ndenumerate(array):
        maze[idx] = bin(int(x))[2:].zfill(5)
    display_array = np.pad(array, 1, mode="constant", constant_values=31)
    display_maze  = np.zeros_like(display_array).astype(str)
    for idx, x in np.ndenumerate(display_array):
        display_maze[idx] = bin(int(x))[2:].zfill(5)
    return maze, display_maze


def generate_weights(row, column):
    temp_weights = np.zeros((row, column, 4), dtype=str)
    for idx, x in np.ndenumerate(temp_weights):
        i, j, k = idx
        if j == 0:
            temp_weights[i,j][3] = str(random.randint(1,9))
        else:
            temp_weights[i,j][3] = temp_weights[i,j-1][2]
        temp_weights[i,j][2] = str(random.randint(1,9))
        if i == 0:
            temp_weights[i,j][0] = str(random.randint(1,9))
        else:
            temp_weights[i,j][0] = temp_weights[i-1,j][1]
        temp_weights[i,j][1] = str(random.randint(1,9))

    weights = np.empty((row, column))  # Create an empty array to hold the final values
    for idx, x in np.ndenumerate(weights):
            ele = ''.join(temp_weights[idx])
            weights[idx] = str(ele)
    weights = weights.astype(int).astype(str)

    for idx, x in np.ndenumerate(weights):
            if len(weights[idx]) == 3:
                weights[idx]='0'+weights[idx]
    return weights

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
    solver_visited.append([(1,1)])
    end = (rows-1,columns-1)
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


# rows = 30
# columns = 30 
# array = np.full((rows,columns), 15)

# i = np.random.randint(0,rows)
# j = np.random.randint(0,columns)
# visited = []
# visited.append((1,2))
# # maze, display_maze = prims_algo_random(array, visited)
# # print(display_maze)

# '''[['11111', '11111', '11111', '11111', '11111'],
#  ['11111', '01101' ,'01010' ,'01011' ,'11111'],
#  ['11111', '01101', '00000' ,'00010' ,'11111'],
#  ['11111', '01101' ,'00110' ,'00111' ,'11111'],
#  ['11111', '11111' ,'11111' ,'11111', '11111']]'''

# maze, display_maze = prims_algo_notrandom(array, visited)
# view_wall_group = pygame.sprite.Group()
# game_screen.view_maze(display_maze, view_wall_group)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#     screen.fill("black")
#     view_wall_group.draw(screen)
#     pygame.display.update()



