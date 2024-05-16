import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x,y,type="flappy_bird"):
        super().__init__()
        self.image = pygame.image.load("maze_images/steve/steve_front_1.png").convert_alpha()

        # starts at the beginning of the maze

        self.rect = self.image.get_rect(topleft = (370,420))
        self.x = x
        self.y = y
        self.pos_x = 240
        self.pos_y = 240

        # these parameters are for the display functionality

        self.maze_i = y // 120
        self.maze_j = x // 120

        # self.inventory = {"speed_pot":1, "health_pot":1, "marker":1, "elytra":1, "enchanted_gapple":1, "totem":1, "strength_pot":1}
        self.inventory = {}
        self.health = 10

        self.inventory_full = False
        self.weapon = "wooden_sword"

        self.inventory_spot = 1
        self.score = 0
        self.attack_tick = 0
        self.strength = 1
        self.org_strength = 1
        self.damage_received = 0.05
        self.org_damage_received = 0.05
        self.strength_effect_time = 5
        self.swiftness_effect_time = 5
        self.resistance_effect_time = 5
        self.collision_where = ''
        self.time_left = None
        self.total_time = None
        self.load_inventory = False
        self.enemy_where = ''
        self.enemy_collision_tick = 0
        self.dt = 0
        self.weapon_level = 1
        self.attack_radius = 120

        # loading the frames for the player

        self.right_frames = [pygame.image.load(f"maze_images/steve/steve_right ({i}).png") for i in range(1,6)]
        self.left_frames = [pygame.image.load(f"maze_images/steve/steve_left ({i}).png") for i in range(1,6)]
        self.up_frames = [pygame.image.load(f"maze_images/steve/steve_back_{i}.png") for i in range(1,6)]
        self.down_frames = [pygame.image.load(f"maze_images/steve/steve_front_{i}.png") for i in range(1,6)]
        self.animation_index = 0

        self.damaged_surf = pygame.image.load("maze_images/steve_nobg/steve_damaged.png").convert_alpha()
        self.direction = "down"


    def animate(self):

        # according to which direction the player is trying to move, the direction would be changed accordingly from the wall class

        frames = []
        if self.direction == "right": frames = self.right_frames
        if self.direction == "left": frames = self.left_frames
        if self.direction == "up": frames = self.up_frames
        if self.direction == "down": frames = self.down_frames
        if frames:

            # blitting in the frames for a greater amount of time due to limited number of frames avaiable

            self.image = frames[int(self.animation_index)]
            self.animation_index += 0.3 * 60 * self.dt
            if self.animation_index >= 5: self.animation_index = 0

        else:

            # if the player stops the default image is loaded

            self.image = pygame.image.load("maze_images/steve/steve_front_1.png").convert_alpha()

    
    # reset function when a new maze is generated

    def reset(self):
        self.rect.x = 360
        self.rect.y = 410
        self.x = 0
        self.y = 0
        self.maze_i = self.y // 120
        self.maze_j = self.x // 120
        self.health = 10
        self.strength = self.org_strength
        self.damage_received = self.org_damage_received
        self.inventory = {}
        self.score = 0
        self.time_left = None
        self.total_time = None
        self.weapon_level = 1
        self.enemy_where = ''
        self.enemy_collision_tick = 0
        self.dt = 0
        self.weapon_level = 1
        self.attack_radius = 120

        self.inventory_full = False

    def update(self, reset):
        if reset: self.reset()
        self.animate()
    