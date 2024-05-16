import pygame
import numpy

collision_event = pygame.USEREVENT + 2

# class for an individual wall 

class Wall(pygame.sprite.Sprite):

    def __init__(self,where, factor):
        super().__init__()
        wall = numpy.random.choice(['stone', 'coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore', 'lapis_ore', 'emerald_ore', 'redstone_ore'], p = [0.95, 0.02, 0.01, 0.003, 0.001, 0.0075, 0.001, 0.0075])
        self.image = pygame.image.load(f'maze_images/{wall}.png').convert_alpha()
        
        # in order to render according to the screen size, this idea of factor was implemented

        scale_down = self.image.get_height()
        self.image = pygame.transform.rotozoom(self.image, 0, factor/scale_down)
        self.rect = self.image.get_rect(topleft = where)
        self.collision_where =''

        self.dx = 3

    def move_walls(self,player,obstacle_group,collision_where,dx):
        self.dx = dx
        keys = pygame.key.get_pressed()
        move = ''


        self.collision_where = ''

        # the walls are being moved opposite to what the player presses -> left implies the walls move right, so that relatively 
        # the player looks as if they are moving to the left

        # the player's direction is updated which is used for animating the player

        if keys[pygame.K_UP] and "up" not in player.enemy_where: 
            self.rect.y += self.dx
            player.direction = "up"

            if player.rect.colliderect(self.rect): self.collision_where += "up"
            
        if keys[pygame.K_DOWN] and "down" not in player.enemy_where: 
            self.rect.y -= self.dx
            player.direction = "down"

            if player.rect.colliderect(self.rect): self.collision_where += "down"
        
        if keys[pygame.K_RIGHT] and "right" not in player.enemy_where: 
            self.rect.x -= self.dx
            player.direction = "right"

            if player.rect.colliderect(self.rect): self.collision_where += "right"
                
        if keys[pygame.K_LEFT] and "left" not in player.enemy_where: 
            self.rect.x += self.dx
            player.direction = "left"

            if player.rect.colliderect(self.rect): self.collision_where += "left"

        
        # if no key is pressed, the player's direction is set to stop

        if not(keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]):
            player.direction = "stop"

        
        # if the player collides, an event with information of what side the collision happened is broadcast

        if player.rect.colliderect(self.rect):
            player.collision_where = self.collision_where
            myevent = pygame.event.Event(collision_event, message = self.collision_where)
            pygame.event.post(myevent)
        return move
        
    def update(self, player, obstacle_group,collision_where,dx):
        self.move_walls(player,obstacle_group,collision_where,dx)
        collision(obstacle_group,player)

# this function checks for the collision of the player, and reverts the walls back to their original position

def collision(wall_group,player):
    collision_where = ''
    for wall in pygame.sprite.spritecollide(player, wall_group, False):
        collision_where = wall.collision_where
        break
    keys = pygame.key.get_pressed()

    if collision_where:
        for wall in wall_group:
            dx = wall.dx

            # the first two blocks check whether the player is colliding on two sides, if yes they revert accordingly

            if (keys[pygame.K_UP] and "up" in collision_where):
                if (keys[pygame.K_LEFT] and "left" in collision_where):
                    wall.rect.x -= dx
                elif (keys[pygame.K_RIGHT] and "right" in collision_where) :
                    wall.rect.x += dx
                wall.rect.y -= dx


            elif (keys[pygame.K_DOWN] and "down" in collision_where):
                if (keys[pygame.K_LEFT] and "left" in collision_where):
                    wall.rect.x -= dx
                elif (keys[pygame.K_RIGHT] and "right" in collision_where):
                    wall.rect.x += dx
                wall.rect.y += dx


            # these two blocks are for collisions are only horizontal

            elif (keys[pygame.K_RIGHT] and "right" in collision_where): wall.rect.x += dx

            elif (keys[pygame.K_LEFT] and "left" in collision_where):  wall.rect.x -= dx