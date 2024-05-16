import pygame
import numpy as np
from user_interface import Text
from wall_class import Wall
from collectables import Collectable
import enemy_class
import inventory
import prims_algo
import wall_class
import path_finder

collectables = ["coin", "speed_pot", "health_pot", "marker", "elytra", "enchanted_gapple", "totem", "strength_pot","clock"]

# initialising the maze array and visited list for prims

def initialise(rows, columns):
    array = np.full((rows,columns), 15)
    i = np.random.randint(0,rows)
    j = np.random.randint(0,columns)
    visited = []
    visited.append((i,j))
    return array, visited


# adding the health, time and score on top into a group

def add_text(text_group):

    font = 'font/Pixeltype.ttf'
    text_group = pygame.sprite.Group()
    text_group.add(Text("Health", 35, "black", font, (200,30),False))
    text_group.add(Text("Time left", 35, "black", font, (480,30),False))

    return text_group

# for the elytra collectable -> displaying entire maze

def view_maze(to_render, view_wall_group):
    width = height = 600
    r,c = np.shape(to_render)


    j_fact = width // r
    j_fact = j_fact - j_fact % 2
    i_fact = height // c
    i_fact = i_fact - i_fact % 2

    wall_height = i_fact/2
    wall_width = j_fact/2


    for i in range(r):
        for j in range(c) :
            wall_bit = to_render[i,j] # has bits representing walls in "bnsew" form  b -> boudnary of the maze

            # each cell has four spaces where walls can be put in, the code checks whether there is a south and east wall
            # in the to_render array and adds them into the group if yes

            for k in range(4):
                inner_i = (k // 2) * wall_height
                inner_j = (k % 2) * wall_width

                # adding an offset to make it centered

                where = (j*j_fact + inner_j + (width - c*j_fact)//2, i*i_fact + inner_i + (height + 100 - r*i_fact)//2)
                if (k == 3) or (k == 1 and wall_bit[3] == '1') or (k == 2 and wall_bit[2] == '1'):
                    view_wall_group.add(Wall(where=where, factor = wall_height))

                # checks for the boundary of the maze

                if (k==0) and wall_bit[0] == '1':
                    view_wall_group.add(Wall(where=where, factor = wall_height))


# the function adds walls in respective places considering 360,410 as center cell's topleft where the player is present

def display(player, maze,wall_group,path_group,collectables_group,enemy_group):
    rows, columns = np.shape(maze) # 5 X 5
    i_min = j_min = 0
    i_max = rows
    j_max = columns

    i_start = 2 - (player.maze_i - i_min)
    i_end = 2 + (i_max - player.maze_i)
    j_start = 2 - (player.maze_j - j_min)
    j_end = 2 + (j_max - player.maze_j)

    for i in range(i_start, i_end ):
        for j in range(j_start, j_end):
            wall_bit = maze[player.maze_i + i - 2,j + player.maze_j - 2]
            for k in range(4):
                inner_i = (k // 2) * 60
                inner_j = (k % 2) * 60
                where = (j*120 + inner_j , i*120 + inner_i + 50)

                # similar logic to the above

                if ((i != i_end - 1) and (j != j_end - 1)) and ((wall_bit[0] == '1') or (k == 3) or (k == 1 and wall_bit[-2] == '1') or (k == 2 and wall_bit[-3] == '1')):
                    wall_group.add(Wall(where=where, factor = 60))

                elif (i == i_end - 1 and (j != j_end - 1)) and  (k == 1 or k == 0):
                    wall_group.add(Wall(where=where, factor = 60))

                elif (j == j_end -1 and (i != i_end - 1)) and (k == 0 or k == 2):
                    wall_group.add(Wall(where=where, factor = 60))

                elif j == j_end -1 and i == i_end - 1  and k == 0:
                    wall_group.add(Wall(where=where, factor = 60))

                else:
                    
                    # if the spot is not a wall, it is added to the path_group

                    path_group = np.append(path_group, np.array(where, ndmin=2), axis=0)
    
    # checks for the possible points in the path_groups so as to not render outside the maze or on the player

    poss_points = []
    for i in path_group:
        point = list(i)
        if 0 < point[0] < 300 + 120*(rows-2) and point[1] < 350 + 120*(columns-2) and point != [360, 410]:
            poss_points.append(point)

    # spots for collectables and enemies are chosen
    
    chosen_indices = np.random.choice(len(poss_points), n_enemies+n_collectables, replace = False)
    index_coll = chosen_indices[:n_collectables]
    index_enemy = chosen_indices[n_collectables:]

    # collectables are chosen randomly and put in corresponding spots

    chosen_points = [[poss_points[i][0]+30,poss_points[i][1]+30] for i in index_coll]
    items = np.random.choice(["coin", "speed_pot", "health_pot", "marker", "elytra", "enchanted_gapple", "totem", "strength_pot","clock", "wooden_sword", "stone_sword","iron_sword", "golden_sword", "diamond_sword"],p = [],size=n_collectables)
    for chosen_point in chosen_points:
        if chosen_point != [390, 440]:
            collectables_group.add(Collectable(where = tuple(chosen_point), type=items[chosen_points.index(chosen_point)]))

    # enemies are put in corresponding spots

    chosen_points = [[poss_points[i][0]+30,poss_points[i][1]+30] for i in index_enemy]
    for chosen_point in chosen_points:
        enemy = enemy_class.Enemy(chosen_point, "zombie")
        if not(player.rect.colliderect(enemy.rect)):    
            enemy_group.add(enemy)
    return path_group
                    


def fgenerate_new(level):
    # returns rows, columns, total_time, n_collectables, n_enemies, p_enemies, strength_effect_time, resistace_effect_time, swiftness_effect_time, strength of player and damage received, attack radius
    if level == "Easy":
        rows = columns = 10
        return rows, columns, 60, 10, 8,[0.1,0.1,0.1,0.2,0.1,0.05,0.00625,0.1,0.05,0.1,0.05,0.025,0.0125,0.00625], 5, 5, 5, 0.3, 0.02, 120

    elif level == "Medium":
        rows = columns = 14
        return rows, columns, 120, 20, 16, [0.1,0.1,0.1,0.2,0.1,0.05,0.00625,0.1,0.05,0.1,0.05,0.025,0.0125,0.00625], 8, 8, 8, 0.3, 0.04, 160

    elif level == "Hard":
        rows = columns = 16
        return rows, columns, 180, 25, 20, [0.1,0.1,0.1,0.2,0.1,0.05,0.00625,0.1,0.05,0.1,0.05,0.025,0.0125,0.00625], 12, 12, 12, 0.3, 0.06, 200

# when the level is selected, this function is called

def generate_based_on_level(level,player,wall_group, collectables_group, enemy_group, path_group, inventory_group, start_end_grp):

            global n_collectables, n_enemies, p_collectables

            initialiser = fgenerate_new(level)
            rows, columns = initialiser[0], initialiser[1]
            player.total_time = initialiser[2]
            n_collectables, n_enemies = initialiser[3], initialiser[4]
            p_collectables = initialiser[5]
            player.strength_effect_time, player.resistance_effect_time, player.swiftness_effect_time = initialiser[6], initialiser[7], initialiser[8]
            player.org_strength, player.org_damage_received = initialiser[9], initialiser[10]
            player.strength = player.org_strength
            player.damage_received = player.org_damage_received
            player.attack_radius = initialiser[11]
            # surface for the beginning and the end of the maze

            start_text = inventory.Marker(where = (360, 430), path = "maze_images/start.png")
            end_text = inventory.Marker(where = (300 + columns * 120 - 60, 380 + rows * 120 - 60), path = "maze_images/end.png")

            start_end_grp.add(start_text)
            start_end_grp.add(end_text)

            # creating the maze according to the difficulty

            array, visited = initialise(rows, columns)
            maze,display_maze = prims_algo.prims_algo_random(array, visited)
            path_group = display(player, display_maze, wall_group, path_group, collectables_group, enemy_group)[1:]
            path_finder.solver(maze, rows, columns, "path.txt")

            # initialising the inventory

            inventory.initialise_inventory(player,inventory_group)
            return path_group, maze, display_maze, rows, columns, end_text


# the heart of the program, the game engine function

def game_engine(time_left,wall_group,screen,text_group,start, tot_time,player,path_group,collectables_group,collision_where,dx, inventory_group,selected_slot,enemy_group,attack,marker_group,start_end_grp, level, generate_new,bg_rect):

        font = 'font/Pixeltype.ttf'
        top_surf = pygame.image.load("maze_images/top.png").convert_alpha()
        top_rect = top_surf.get_rect(topleft=(0,0))
        bot_rect = top_surf.get_rect(bottomright = (600,700))

        full_heart_surf = pygame.image.load("maze_images/minecraft_heart.png").convert_alpha()
        half_heart_surf = pygame.image.load("maze_images/half-heart.png").convert_alpha()
        empty_heart_surf = pygame.transform.rotozoom(pygame.image.load("maze_images/empty-heart-1.png").convert_alpha(), 0, 1/20)
        heart_rects = []
        for i in range(5):
            heart_rects.append(full_heart_surf.get_rect(center = (250 + 30*i,30)))
        
        # moves the path group, but this has become redundant

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            path_group = path_group + np.array([0,2])
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            path_group = path_group + np.array([2,0])
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            path_group = path_group + np.array([0,-2])
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            path_group = path_group + np.array([-2,0])

        # all updates and bliting of groups
        
        wall_group.update(player, wall_group, collision_where,dx)

        wall_group.draw(screen)

        if pygame.sprite.spritecollideany(player, enemy_group) == None:
            player.enemy_where = ''

        
        # markers used by the player

        marker_group.draw(screen)
        marker_group.update(collision_where,dx,player)

        collectables_group.update(player, collectables_group,collision_where,dx)
        collectables_group.draw(screen)

        enemy_group.draw(screen)
        enemy_group.update(player,wall_group, enemy_group,collision_where,dx,attack)

        # displays the hotbar

        inventory_group.draw(screen)  
        inventory_group.update(inventory_group,player,selected_slot,screen)

        
        # displays the start and end of the maze

        start_end_grp.draw(screen)
        start_end_grp.update(collision_where,dx,player)

        screen.blit(top_surf, top_rect)

        # displays the health, score, time

        text_group.draw(screen)
        text_group.update()

        # health calculation, and based on health, the hearts are rendered accordingly

        health = int(player.health)
        full = heart_rects[:health//2]
        half = heart_rects[health//2:health//2 + health%2]
        empty = heart_rects[health//2+health%2:]
        for rect in full:
            screen.blit(full_heart_surf, rect)
        for rect in half:
            screen.blit(half_heart_surf, rect)
        for rect in empty:
            screen.blit(empty_heart_surf, rect)

        # checking how many time passed
        
        time_passed = (pygame.time.get_ticks() - start)//1000

        time_left = tot_time - time_passed

        time_group = pygame.sprite.GroupSingle()
        time_group.add(Text(str(time_left), 35, "black", font, (560,30), False))

        # changing the score according to the number of coins the player has and displaying it

        
        
        # displaying the score

        score_group = pygame.sprite.GroupSingle()
        score_group.add(Text(f"Score : {player.score}", 35, "black", font, (60,30), False))
        score_group.draw(screen)
        time_group.draw(screen)
        return time_left            # returning the time left as it is used in the mainloop

        
