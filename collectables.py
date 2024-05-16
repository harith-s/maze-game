import pygame
import numpy as np
import random
class Collectable(pygame.sprite.Sprite):
    def __init__(self, where,type):
        super().__init__()

        # types = ["coin", "elytra", "speed_potion", "health_potion", "enchanted_gapple", "totem", "strength_potion", "marker"]

        # loads the image according to the type

        self.image = pygame.image.load(f"maze_images/{type}.png").convert_alpha()
        self.rect = self.image.get_rect(center = where)
        self.type = type
        self.where = where

        # since collectables also have to move with the maze, even they have a dx

        self.dx = 3

    # the variable collision_where is gotten from the event broadcast when the player collides with the wall

    def move(self,player,collision_where,dx):
        keys = pygame.key.get_pressed()
        self.collision_where = ''
        self.dx = dx
        collision_where = player.collision_where
        # this function reverts the position if the player has collided with the wall
        # additionally, they make this nice moving animation when the player tries to push into the wall, which give the feeling that
        # the player can't go into the wall, a sort of shake
        
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
            
    # if the player collides with the collectable, it is put in his inventory

    def collision(self,player, collectable_group):
        if len(player.inventory) == 8:
            player.inventory_full = True
        else:
            player.inventory_full = False
        if self.type in ["clock", "coin"]:
            if player.rect.colliderect(self.rect):
                if self.type == "clock":
                    player.total_time += 10
                elif self.type == "coin":
                    player.score += 200

                collectable_group.remove(self)
                self.kill()
        elif player.rect.colliderect(self.rect):
            if not(player.inventory_full) and player.inventory.get(self.type) == None:
                    player.inventory[self.type] = 1
                    collectable_group.remove(self)
                    self.kill()
                    player.load_inventory = True


            elif player.inventory.get(self.type) != None:
                player.inventory[self.type] += 1
                collectable_group.remove(self)
                self.kill()
                player.load_inventory = True

    
    def update(self, player, collectable_group,collision_where,dx):
        self.move(player,collision_where,dx)
        self.collision(player, collectable_group)

# animation for the totem of undying when the player dies but has a totem in their inventory

def totem_animation(screen,wall_group,collectable_group, marker_group,enemy_group,player,totem_i,effects,bg, bg_rect, totem_sound, totem_channel):
    # totem_channel.play(totem_sound)

    # in total there are 37 frames for the animation
    totem_surface = pygame.image.load(f"maze_images/totem_frames/totem_f (1).gif").convert_alpha()
    totem_rect = totem_surface.get_rect(center = (300,350))
    if totem_i < 37:
        totem_surface = pygame.image.load(f"maze_images/totem_frames/totem_f ({int(totem_i)}).gif").convert_alpha()
        totem_rect = totem_surface.get_rect(center = (300,350))

    # the offset is to ensure a slower and smoother animation

    totem_i += 0.2 * 60 * player.dt

    # all the groups except the top rectangle groups are drawn on screen, which gives this dramatic effect of the person dying but coming back to life

    screen.blit(bg, bg_rect)
    screen.blit(player.image, player.rect)
    wall_group.draw(screen)
    marker_group.draw(screen)
    collectable_group.draw(screen)
    enemy_group.draw(screen)
    screen.blit(totem_surface, totem_rect)

    # once all frames have been rendered, control is transfered back to the main loop
    # a few effects are also given to the player
    # no matter how many totems the person collects, at a time, all totems are deleted after the person has used up a totem

    if totem_i > 37:
        player.health = 5
        del player.inventory["totem"]
        player.strength = 5
        player.damage_received = 0.01
        effects.append("strength")
        effects.append("resistance")
    return totem_i

