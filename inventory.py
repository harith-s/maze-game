import pygame
import numpy as np
from user_interface import Text
import collectables

# inventory class, for each square in the hotbar

class Inventory(pygame.sprite.Sprite):
    def __init__(self, slot, contains,number):
        super().__init__()

        # surfaces

        self.selected = pygame.image.load("maze_images/inventory_selected.png").convert_alpha()
        self.unselected = pygame.image.load("maze_images/inventory_unselected.png").convert_alpha()

        self.image = self.unselected

        # this is for calculating where to blit the slot

        i = 50 * slot
        self.slot = slot % 10 + 48
        self.rect = self.image.get_rect(topleft = (i+50, 650))
        
        # what does the slot contain and how many

        self.contains = contains
        self.number = number

        self.contains_item = None
        self.contains_rect = None
        self.number_sprite = None
        

    def update(self,inventory_group,player,selected_slot,screen):
        if player.load_inventory: load_stuff(inventory_group, player,selected_slot,screen)
        if self.contains_item != None: screen.blit(self.contains_item, self.contains_rect)
        if self.number_sprite != None: screen.blit(self.number_sprite.image, self.number_sprite.rect)


def new_load_stuff(inventory_group,player,selected_slot,screen):
    d = player.inventory
    dict_keys = list(d.keys())
    for i in dict_keys:
        for inventory in inventory_group:
            if inventory.contains == i:
                inventory.number = d[i]
                inventory.number_sprite.level = f"{d[i]}"
                inventory.number_sprite.image = inventory.number_sprite.font.render(f"{d[i]}", True, (255,255,255))
                break
        else:
            for inventory in inventory_group:
                if inventory.contains == None:
                    inventory.contains = i
                    inventory.number = d[i]
                    inventory.number_sprite.level = f"{d[i]}"
                    inventory.number_sprite.image = inventory.number_sprite.font.render(f"{d[i]}", True, (255,255,255))
                    break





def load_stuff(inventory_group,player,selected_slot,screen):
    
    # inventory is updated constantly 

    inventory_group.empty()
    d = player.inventory
    

    dict_keys = list(d.keys())
    for i in range(1,9):
        if i - 1 < len(dict_keys):
            contains = dict_keys[i - 1]
            number = d[dict_keys[i - 1]]
        else:
            contains = None
            number = 0

        # this relies on the property that dictionaries are ordered
        # if there is something at some spot, it puts it in the inventory

        inventory_group.add(Inventory(i, contains, number))
    
    # if a slot is selected, it changes the image of that 

    if selected_slot != None:
        for inventory in inventory_group:
            
            inventory.image = inventory.unselected
            if inventory.slot == selected_slot:
                inventory.image = inventory.selected

    font = 'font/minecraft_font.ttf'

    # displays the item present in the inventory of the player and the number as well

    for inventory in inventory_group:
        if inventory.contains != None:
            inventory.contains_item = pygame.image.load(f"maze_images/{inventory.contains}.png").convert_alpha()
            
            if inventory.number != 48: 
                inventory.number_sprite = Text(f"{inventory.number}", 16, (255,255,255), font = font, where = (50 * (inventory.slot - 48 + 1) + 40, 650 + 40), should_i_update=False)
                inventory.contains_rect = inventory.contains_item.get_rect(topleft = (50 * (inventory.slot - 48 + 1) + 10, 650 + 10))
            else:
                inventory.number_sprite = Text(f"{inventory.number}", 16, (255,255,255), font = font, where = (500 + 40, 650 + 40), should_i_update=False)
                inventory.contains_rect = inventory.contains_item.get_rect(topleft = (450 + 10, 650 + 10))

            

# returns which collectable the player wants to use

def use_collectable(player, item,selected_slot):

    # 49 because the ascii value of 1 is 49 and 1 is first slot, for 0 -> 48 goes to the last slot 
    
    dict_keys = list(player.inventory.keys())
    try:
        item = dict_keys[selected_slot - 49]
        if item not in ["totem", "wooden_sword","stone_sword", "iron_sword", "gold_sword", "diamond_sword"]: player.inventory[item] -= 1
        if player.inventory[item] == 0:
            del player.inventory[item]
    except:
        item = None
    return item

# initialises the inventory when the maze is created
 
def initialise_inventory(player,inventory_group):
    dict_keys = list(player.inventory.keys())
    for i in range(1,9):
        if i - 1 < len(dict_keys):
            contains = dict_keys[i - 1]
            number = player.inventory[dict_keys[i - 1]]
        else:
            contains = None
            number = 0
        inventory_group.add(Inventory(i, contains,number)) 
    player.load_inventory = True


# this class for the collectacle marker and the start and end markers
     
class Marker(pygame.sprite.Sprite):
    def __init__(self, where = (380, 410), path = "maze_images/redstone_torch.png"):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        # 360, 410 because that is where the player is
        
        if where == (380, 410): 
            # this is for the  markers

            self.rect = self.image.get_rect(center = where)
        else: 
            # this is for the start and end markers

            self.rect = self.image.get_rect(topleft = where)

        self.dx = 3


    # if all walls are moving then the marker moves otherwise it stays in the same place
    # collision_where tells where the collision is happening

    def move_marker(self,dx, collision_where,player):
        self.dx = dx
        keys = pygame.key.get_pressed()

        collision_where = player.collision_where

        if keys[pygame.K_RIGHT]: 
            self.rect.x -= self.dx
        if "right" in collision_where or ("right" in player.enemy_where and keys[pygame.K_RIGHT]):
            self.rect.x += self.dx

        if keys[pygame.K_LEFT]: 
            self.rect.x += self.dx
        if "left" in collision_where or ("left" in player.enemy_where and keys[pygame.K_LEFT]):
            self.rect.x -= self.dx
            
        if keys[pygame.K_UP]: 
            self.rect.y += self.dx
        if "up" in collision_where or ("up" in player.enemy_where and keys[pygame.K_UP]):
            self.rect.y -= self.dx
        
        if keys[pygame.K_DOWN]: 
            self.rect.y -= self.dx
        if "down" in collision_where or ("down" in player.enemy_where and keys[pygame.K_DOWN]):
            self.rect.y += self.dx
        
    def update(self,collision_where,dx,player):
        self.move_marker(dx, collision_where,player)


def drop_collectable(player, selected_slot, collectables_group, wall_group):
    dict_keys = list(player.inventory.keys())
    try:
        item = dict_keys[selected_slot - 49]
        player.inventory[item] -= 1
        if player.inventory[item] == 0:
            del player.inventory[item]
        player.load_inventory = True
        x , y = player.rect.center
        poss_spots = [collectables.Collectable((x-60,y), item), collectables.Collectable((x+60,y), item), collectables.Collectable((x,y+60), item), collectables.Collectable((x,y+60), item)]
        temp = list(poss_spots)
        for spot in temp:
            if pygame.sprite.spritecollide(spot, wall_group, False):
                poss_spots.remove(spot)
                print(spot)
        
        collectables_group.add(np.random.choice(poss_spots))
    except:
        pass