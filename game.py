import pygame
import numpy as np
from player import Player
from wall_class import Wall
import user_interface
import game_screen
import inventory
import collectables

# north = 8, south = 4, east = 2, west = 1

# function to reset groups when generating a new maze

def reset(player_group, groups_to_reset, path_group):
    player_group.update(True)
    for group in groups_to_reset:
        group.empty()
    path_group = np.array([[-1,-1]])
    return path_group, True

# initialisation of parameters

height = 600
width = 600

pygame.init()
screen = pygame.display.set_mode((600,700))
pygame.display.set_caption("maze game")

clock = pygame.time.Clock()
running = True

potion = pygame.mixer.Channel(0)
totem = pygame.mixer.Channel(1)


# level represents the difficulty chosen, phase is whether the user is playing or at the user_interface
# v the velocity done when the player presses a key
# selected_slot is the selected inventory slot

global level
level = ''
phase = 'interface' 
v = 300
selected_slot = None
time_left = None # doesn't represent anything
font = pygame.font.Font('font/minecraft_font.ttf', 80)
framerate = 60
dt = 1/framerate

# surface imports 

# title card
welcome_surface = font.render("Mazerunner", True, "white")
welcome_rect = welcome_surface.get_rect(center = (300,150))

# mouse cursor surface

mouse_hyperlink = pygame.transform.rotozoom(pygame.image.load("maze_images/cursor-removebg-preview.png").convert_alpha(),0,0.3)
mouse_normal = pygame.transform.rotozoom(pygame.image.load("maze_images/no-hyper-cursor-removebg-preview.png").convert_alpha(),0,0.05)

# effect status and animations surface imports

swiftness = pygame.image.load("maze_images/swiftness_effect.png").convert_alpha()
swiftness_rect = swiftness.get_rect(topleft = (560, 650))
strength = pygame.image.load("maze_images/strength_effect.png").convert_alpha()
strength_rect = strength.get_rect(topleft = (580, 650))
totem_surface = pygame.image.load("maze_images/totem_frames/totem_f (1).gif").convert_alpha()
totem_rect = totem_surface.get_rect(center = (400, 300))
bg = pygame.image.load("maze_images/stone_bg.png").convert_alpha()
bg_rect = bg.get_rect(topleft = (0,50))


# music and sounds

pygame.mixer.music.load("maze_sounds/pigstep.mp3")
pygame.mixer.music.set_volume(0.1)
totem_activated = pygame.mixer.Sound("maze_sounds/totem_activated_shortened.mp3")
potion_activated = pygame.mixer.Sound("maze_sounds/potion_activated.mp3")

# # GROUPS # #

# the ones which are added in game.py itself, doesn't depend on the level

level_group = pygame.sprite.Group() 

player_group = pygame.sprite.GroupSingle()

mouse_group = pygame.sprite.GroupSingle()

game_text_grp = pygame.sprite.Group()

game_over = pygame.sprite.Group()

view_wall_group = pygame.sprite.Group()

marker_group = pygame.sprite.Group()

mainmenu_group = pygame.sprite.Group()

how_to_play_group = pygame.sprite.Group()

settings_group = pygame.sprite.Group()

graphics_group = pygame.sprite.Group()

music_group = pygame.sprite.Group()

sound_group = pygame.sprite.Group()

background_group = pygame.sprite.Group()

music_text_group = pygame.sprite.Group()

sound_text_group = pygame.sprite.Group()


# the ones which depend on the level and hence are added in game_screen

wall_group = pygame.sprite.Group()

collectables_group = pygame.sprite.Group()

inventory_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

start_end_grp = pygame.sprite.Group()

score_group = pygame.sprite.Group()

path_group = np.array([[-1,-1]]) # store path list as an array to speed up calculations


# the groups to be reset for play again and back to menu

groups_to_reset = [wall_group, collectables_group, inventory_group, enemy_group, start_end_grp, view_wall_group, marker_group,score_group]



# adding sprites in groups

user_interface.add_text(mainmenu_group, level_group, game_over, settings_group, graphics_group, music_group, sound_group, background_group, how_to_play_group, music_text_group, sound_text_group)

player = Player(0,0)
player_group.add(player)
player.dt = dt 

mouse_group.add(user_interface.Mouse(mouse_normal=mouse_normal, mouse_hyperlink=mouse_hyperlink))

game_text_grp = game_screen.add_text(game_text_grp)


# # events

level_pressed = pygame.USEREVENT + 1         # checks which level was pressed
collision_event = pygame.USEREVENT + 2       # event to check on what side of the player collision has happened
explosion_event = pygame.USEREVENT + 3       # event to check if a creeper has exploded

# initialisations for variables which are changed in the course of the game 
# time_<effect> is to control the amount of time the effect lasts

start = time_speed_pot = time_view = gapple_time = strength_time = time_totem = pygame.time.get_ticks() 
total_time = None

view = False     # view is for the elytra collectable

attack = False   # stores whether the player is attacking

item = None      # stores which item the player plans to use

effects = []     # for displaying the status effect below

win = False      # whether ther person has finished the game

totem_i = 1      # for totem animation after the player dies

generate_new = True # stores whether a new maze is needed 

added = False      # stores whether the game_over text has been added to the group

totem_used = False  # stores whether the totem has been used

menu = "main"       # stores which menu is being displayed

button = None       # stores which button is pressed

option = None       # stores which option is pressed

totem_sound_played = False # stores whether totem sound has been played

mouse_down = False     # stores whether the mouse button is down

sound = True       # stores whether the sound is on or off 

pygame.mixer.music.play(-1)



while running:
    
    # this tick speed is to ensure that when rect collide the player doesn't take damage because space bar isn't pressed fast enough
    if player.attack_tick % 20 == 0:
        attack = False
    use = False      # stores whether the player wants to use something
    drop = False     # stores whether the player wants to drop something
    player.load_inventory = False
    collision_where = ''  # stores where the collision is happening
    player.collision_where = ''
    mouse_down = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True  

        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE: # space bar for attack
                attack = True

        elif event.type == collision_event:
            collision_where = event.message
        
        elif event.type == explosion_event:
            explosion_pos_x, explosion_pos_y = event.position
            x, y = player.rect.center
            if abs(explosion_pos_x - x) < 20 and abs(explosion_pos_y - y) < 20:
                player.health -= 4
            elif abs(explosion_pos_x - x) < 30 and abs(explosion_pos_y - y) < 30:
                player.health -= 2
            elif abs(explosion_pos_x - x) < 40 and abs(explosion_pos_y - y) < 40:
                player.health -= 1
            

        if event.type == pygame.KEYDOWN:
            for i in range(1,11):
                if event.key  == i % 10 + 48:      # this is for checking which slot is selected 48 + i -> i in keyboard 
                    selected_slot = i % 10 + 48
                    player.load_inventory = True
                    if selected_slot - 49 < len(list(player.inventory.keys())): 
                        item = list(player.inventory.keys())[selected_slot - 49]
                        if item == "wooden_sword":
                            player.weapon_level = 1.5
                        elif item == "stone_sword":
                            player.weapon_level = 1.8
                        elif item == "iron_sword":
                            player.weapon_level = 2
                        elif item == "golden_sword":
                            player.weapon_level = 2.5
                        elif item == "diamond_sword":
                            player.weapon_level = 4
                        else:
                            player.weapon_level = 1
                        
            if event.key == pygame.K_e:             # does the player want to use?
                use = True 
            if event.key == pygame.K_q:
                drop = True
        if event.type == level_pressed:
            if event.message in ["Play","Level","Settings","How to play","Exit"]:
                menu = event.message
                print(menu)
            if event.message in ["Easy", "Medium", "Hard"]: 
                level = event.message
            if event.message in ["Back", "Graphics", "Music", "Sound", "Background"]:
                button = event.message
            if event.message in ["Low", "Medium", "High"]:
                option = event.message
            if "ON"  in event.message or "OFF" in event.message:
                option = event.message
                if pygame.mixer.music.get_busy() and event.message == "Music OFF":
                    pygame.mixer.music.pause()

                elif not(pygame.mixer.music.get_busy()) and event.message == "Music ON":
                    pygame.mixer.music.unpause()
                
                if event.message == "Sound OFF": sound = False
                elif event.message == "Sound ON": sound = True

            elif event.message == "Play again": 
                start = pygame.time.get_ticks()
                phase = 'interface'
                path_group, generate_new = reset(player_group, groups_to_reset, path_group)   # resets everything and control is transfered to interface, and to play as level is already selected
                added = False
                win = False
                totem_activated = False

            elif event.message =="Back to menu": 
                phase = 'interface'
                menu = "main"
                path_group, generate_new = reset(player_group, groups_to_reset, path_group)  # control transfered to interface
                added = False
                win = False
                totem_activated = False
        

        

    if phase == "interface":
        if menu == "main":
            screen.fill("black")
            user_interface.display_main(screen, welcome_surface,welcome_rect, mainmenu_group, mouse_group)
        elif menu == "Play":
            if level == '':
                level = "Medium"
            if generate_new and level in ["Easy", "Medium", "Hard"]:
                path_group, maze, display_maze, rows, columns,end_text = game_screen.generate_based_on_level(level,player,wall_group, collectables_group, enemy_group, path_group, inventory_group, start_end_grp)
                generate_new = False
                added = False
                phase = 'play'
                player.time_left = player.total_time
                start = pygame.time.get_ticks()

        elif menu == "How To play":
            pass
        elif menu == "Settings":
            user_interface.display_settings(screen, settings_group, mouse_group)
            if button == "Back":
                menu = "main"
                button = None
            if button == "Graphics":
                user_interface.display_graphics(screen, graphics_group, mouse_group)
                
                if option == "Low":
                    framerate = 60
                    player.dt = 1/framerate
                    dt = 1/framerate
                elif option == "Medium":
                    framerate = 80
                    player.dt = 1/framerate
                    dt = 1/framerate

                elif option == "High":
                    framerate = 100
                    player.dt = 1/framerate
                    dt = 1/framerate

                elif button == "Back":
                    menu = "main"
                # print(button)
            elif button == "Music":
                user_interface.display_music(screen, music_text_group, mouse_group)
                if button == "Back":
                    menu = "main"

            elif button == "Sound":
                user_interface.display_sound(screen, sound_text_group, mouse_group)
                if button == "Back":
                    menu = "main"
            elif button == "Background":
                pass
        elif menu == "Level":
            # user_interface.user_display(screen, welcome_surface, welcome_rect, level_group, mouse_group, phase, game_over,win,player,player.time_left, added,score_group, menu, mainmenu_group)
            user_interface.display_level(screen, level_group, mouse_group)
            if generate_new and level in ["Easy", "Medium", "Hard"]:
                path_group, maze, display_maze, rows, columns,end_text = game_screen.generate_based_on_level(level,player,wall_group, collectables_group, enemy_group, path_group, inventory_group, start_end_grp)
                generate_new = False
                added = False
                phase = 'play'
                player.time_left = player.total_time
                start = pygame.time.get_ticks()
            elif button == "Back":
                menu = "main"
                button = None
        if menu == "Exit":
            running = False
            
    

    if phase == "play":
        
        if use:
            item = inventory.use_collectable(player, item, selected_slot)
            player.load_inventory = True
            
            if item == "speed_pot":   # increases the speed of the player
                if sound: potion.play(potion_activated)
                v = 800
                time_speed_pot = pygame.time.get_ticks()//1000
                effects.append("swiftness")
            
            elif item == "elytra":    # shows the top view 

                game_screen.view_maze(display_maze, view_wall_group)
                view = True
                time_view = pygame.time.get_ticks()//1000

            elif item == "health_pot":          # heals the player according to the current health
                    if sound: potion.play(potion_activated)
                    if player.health < 1.5:
                        player.health += 2.5
                    elif player.health < 3.5:
                        player.health += 1.5
                    else:
                        player.health += 1
                    if player.health > 10: player.health = 10

            elif item == "marker":               # places a marker on the maze which moves with the maze

                marker_group.add(inventory.Marker(where = (360,425)))

            elif item == "enchanted_gapple":     # heals the player and gives the player special effects
                player.health = 10
                player.strength = 5
                player.damage_received = 0.01
                effects.append("resistance")
                effects.append("strength")
                gapple_time = pygame.time.get_ticks()//1000

            elif item == "strength_pot":          # increases the attack damage of player
                if sound: potion.play(potion_activated)
                player.strength = 6
                strength_time = pygame.time.get_ticks()//1000
                effects.append("strength")


        # the following is to ensure that effects last for only a certain amount of time
        # this also removes the effects from displaying in the status bar

        if pygame.time.get_ticks()//1000 - time_speed_pot > player.swiftness_effect_time:
            v = 300
            if "swiftness" in effects: effects.remove("swiftness")

        if pygame.time.get_ticks()//1000 - time_view > 5:
                view = False
                player.time_left = player.time_left - 10  # to deincentive too much overuse of this, time passes quicker when the top view is present

        if pygame.time.get_ticks()//1000 - gapple_time > 5:
            player.strength = player.org_strength
            player.damage_received = player.org_damage_received
            if "strength" in effects: effects.remove("strength")
            if "resistance" in effects: effects.remove("resistance")
        
        if pygame.time.get_ticks()//1000 - strength_time > player.strength_effect_time:
            player.strength = player.org_strength
            if "strength" in effects: effects.remove("strength")
            
        if pygame.time.get_ticks()//1000 - time_totem > 5:
            player.strength = player.org_strength
            player.damage_received = player.org_damage_received
            if "strength" in effects: effects.remove("strength")
            if "resistance" in effects: effects.remove("resistance")
    
        if drop:
            inventory.drop_collectable(player, selected_slot, collectables_group, wall_group)

        # if the player's health goes below half a heart, the player dies
        dict_keys = list(player.inventory.keys())
        if player.time_left > 0 and player.health > 1 and not(win):
            if not(view):
                screen.blit(bg, bg_rect)
                pygame.mouse.set_visible(True)
                player.time_left = game_screen.game_engine(player.time_left, wall_group, screen, game_text_grp, start, player.total_time,player,path_group,collectables_group, collision_where,v*dt, inventory_group,selected_slot, enemy_group,attack, marker_group,start_end_grp,level,generate_new,bg_rect)
                player_group.draw(screen)
                player_group.update(reset= False)

                # this is the end rect, once the player reaches it they wins

                if player.rect.colliderect(end_text.rect):
                    win = True

        
            else:

                # for the elytra function

                screen.fill("black")
                pygame.mouse.set_visible(False)
                view_wall_group.draw(screen)

        # for the totem usage
        
        elif player.health < 1 and player.inventory.get("totem") != None and (totem_used == False) and (selected_slot != None and selected_slot - 49 < len(dict_keys) and dict_keys[selected_slot - 49] == "totem") :

            if not(totem_sound_played):
                if sound: totem.play(totem_activated)
                totem_sound_played = True
            totem_i = collectables.totem_animation(screen,wall_group,collectables_group, marker_group,enemy_group,player,totem_i,effects,bg, bg_rect, totem_activated,totem_channel = totem)
            if totem_i > 37:
                time_totem = pygame.time.get_ticks()//1000
                player.load_inventory = True
                totem_used = True
                
        else:
            effects = []
            phase = "end"
            # displays the score, message whether the player won or not, and puts options to go back to menu -> level is rechosen or play again with the same level
            
    if phase == "end":

        player.time_left, added = user_interface.display_end(screen, added, score_group, game_over, win, player, time_left, mouse_group)
    
    # managing effects in the space next to inventory     

    if effects and phase == "play":
        for i in effects:
            if i == "swiftness":
                screen.blit(swiftness, swiftness_rect)
            if i == "strength":
                screen.blit(strength, strength_rect)
    pygame.display.update()
    clock.tick(framerate)
pygame.quit()