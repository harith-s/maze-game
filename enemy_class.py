import pygame
import numpy as np
import random

# class for each enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, where, type):
        super().__init__()
        
        # randomly spawning a zombie or a creeper with some weight

        if random.randint(1,3)>1: 
            self.image = pygame.image.load("maze_images/zombie.png").convert_alpha()
            self.normal_surf = self.image 
            self.damaged_surf = pygame.image.load("maze_images/zombie_damage.png").convert_alpha() 
            self.type = "zombie"
            self.health = 10

        else: 
            self.image = pygame.image.load("maze_images/creeper.png").convert_alpha()
            self.normal_surf = self.image   
            self.exploding = pygame.image.load("maze_images/creeper_exploding.png").convert_alpha()
            self.damaged_surf = pygame.image.load("maze_images/creeper_damaged.png").convert_alpha()
            self.type = "creeper"
            self.health = 10
            
        
        self.rect = self.image.get_rect(center = where)

        self.where = where

        # this is for moving the enemy randomly

        self.direction = random.choice(["up", "down", "left", "right"])
        self.tick = 0           # to control how often the enemy changes directions

        # health of the enemy

        self.activate = False

        self.explode_tick = 0

        # to check whether the creeper died by player or explosion

        self.dead_by_explosion = False


    def move(self, wall_group,player, collision_where, dx):

        keys = pygame.key.get_pressed()
        self.dx = dx
        collision_where = player.collision_where
        # this is to ensure that the enemy moves along with the maze
        

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

        # this part of the movement is for the random movement of the enemy

        if (0 < self.rect.x < 600 or  0 < self.rect.y < 600) and not(player.rect.colliderect(self.rect)):
            
            if abs(self.rect.x - 360) > player.attack_radius or abs(self.rect.y - 410) > player.attack_radius:
                if self.direction == "up":
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.y += 1
                        self.direction = random.choice(["down", "left", "right"])
                        
                elif self.direction == "down":
                    self.rect.y += 1
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.y -= 1
                        self.direction = random.choice(["up", "left", "right"])

                elif self.direction == "left":
                    self.rect.x -= 1
                    if pygame.sprite.spritecollide(self, wall_group,False):
                        self.rect.x += 1
                        self.direction = random.choice(["up", "down", "right"])

                elif self.direction == "right":
                    self.rect.x += 1
                    if pygame.sprite.spritecollideany(self, wall_group):
                        self.rect.x -= 1
                        self.direction = random.choice(["up", "down", "left"])

                self.tick += 1

                # changing the direction after 90 ticks

                if self.tick % 90 == 0:
                        self.direction = random.choice(["down", "left", "right", "up"])
            else:
                if self.rect.x < 360: 
                    self.rect.x += 1
                    if pygame.sprite.spritecollide(self, wall_group,False): 
                        self.rect.x -= 1
                elif self.rect.x > 360:
                    self.rect.x -= 1
                    if pygame.sprite.spritecollide(self, wall_group,False): 
                        self.rect.x += 1
                if self.rect.y < 410:
                    self.rect.y += 1
                    if pygame.sprite.spritecollide(self, wall_group,False): 
                        self.rect.y -= 1
                elif self.rect.y > 410:
                    self.rect.y -= 1
                    if pygame.sprite.spritecollide(self, wall_group,False): 
                        self.rect.y += 1
            
        
            
    def destroy(self, enemy_group,player):

        # if the health is lesser than zero, the sprite is destroyed and the score is increased, for creeper -> if not death by explosion, it increases

        if self.type == "creeper":
            if self.health <= 0:
                if not(self.dead_by_explosion):
                    player.score += 100
                enemy_group.remove(self)
                self.kill()
        else:
            if self.health <= 0:
                player.score += 100
                enemy_group.remove(self)
                self.kill()

    def animate_creeper(self, player):

        # to show the exploding animation
        x,y = player.rect.center
        if self.type == "creeper":
            if self.activate:
                if self.explode_tick % 40 < 20:
                    self.image = self.exploding
                else:
                    self.image = self.normal_surf
            elif abs(self.rect.x -x) > 40 and abs(self.rect.y - y) > 40:
                self.image = self.normal_surf
    # function when player comes in contact with the enemy

    def contact(self,player,attack):

        # the purpose of the attack tick is to ensure that the player doesn't take damange when the player isn't pressing the spacebar fast enough, the attack variable stays true
        # but when the player isn't pressing, the enemy doesn't take damage
        
        # player.enemy_where = ''
        if self.type == "zombie":

            # to make sure that the player doesn't phase through enemies

            if player.rect.colliderect(self.rect):
                if player.rect.y < self.rect.y:
                    if player.rect.x < self.rect.x:
                        player.enemy_where = "downright"
                    else:
                        player.enemy_where = "downleft"
                else:
                    if player.rect.x < self.rect.x:
                        player.enemy_where = "upright"
                    else:
                        player.enemy_where = "upleft"
                keys = pygame.key.get_pressed()

                if attack and keys[pygame.K_SPACE]:  # reduce health of enemy only if the attack tick hasn't reset and the player is pressing space
                    
                    self.health -= player.strength * 60 * player.dt * player.weapon_level
                    self.image = self.damaged_surf

                elif not(attack) and player.attack_tick % 60 == 0: 
                    player.image = player.damaged_surf 
                    player.health -= 0.6 * 60 * player.dt  # if attack tick has reset and the player isn't pressing space, he receives damage

                if not(keys[pygame.K_SPACE]): self.image = self.normal_surf

                player.attack_tick += 1

        elif self.type == "creeper":

            # to make sure that the player doesn't phase through enemies

            if player.rect.colliderect(self.rect):
                if player.rect.y < self.rect.y:
                    if player.rect.x < self.rect.x:
                        player.enemy_where = "downright"
                    else:
                        player.enemy_where = "downleft"
                else:
                    if player.rect.x < self.rect.x:
                        player.enemy_where = "upright"
                    else:
                        player.enemy_where = "upleft"

            # if the player is close enough to the creeper, the creeper explodes

            x,y = player.rect.center
            if abs(self.rect.x -x) < 40 and abs(self.rect.y - y) < 40:
                self.activate = True
                if self.activate:
                    self.explode_tick += 1

                # it is sort of like a time bomb, if the player doesn't move away in time, the creeper explodes

                if self.explode_tick >= 175:
                    myevent = pygame.event.Event(pygame.USEREVENT + 3, position = self.rect.center)
                    pygame.event.post(myevent)
                    self.dead_by_explosion = True
                    self.health = 0
            else: 
                self.explode_tick = 0   # reset the tick if the player moves away
            keys = pygame.key.get_pressed()

            if attack and keys[pygame.K_SPACE] and player.rect.colliderect(self.rect):  # reduce health of enemy only if the attack tick hasn't reset and the player is pressing space
                    self.health -= player.strength * 60 * player.dt * player.weapon_level
                    self.image = self.damaged_surf

            if not(keys[pygame.K_SPACE]): self.image = self.normal_surf
            
            
    def update(self, player, wall_group, enemy_group,collision_where,dx,attack):
        self.move(wall_group,player, collision_where, dx)
        self.contact(player,attack)
        self.destroy(enemy_group,player)
        self.animate_creeper(player)

        
