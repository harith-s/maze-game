import pygame

# in order to change the cursor when hovering over an option which is clickable, the mouse class is implemented

class Mouse(pygame.sprite.Sprite):
    def __init__(self,mouse_normal, mouse_hyperlink):
        super().__init__()

        # loading the normal images and the hyperlink images (the cursor which appears when something is clickable)

        self.image = mouse_normal
        self.rect = mouse_normal.get_rect(center = pygame.mouse.get_pos())
        self.mouse_normal = mouse_normal
        self.mouse_hyperlink = mouse_hyperlink
        self.mouse_click_tick = 0

    def update(self,text_group):

        # the function checks whether the mouse is colliding with the text group, if it does, it changes the cursor position

        self.rect = self.mouse_normal.get_rect(center = pygame.mouse.get_pos())
        if pygame.sprite.spritecollide(self, text_group,False):
            self.image = self.mouse_hyperlink
        else:
            self.image = self.mouse_normal    # if not it reverts back to normal


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pass    

# class of sprite for most text groups within the game

class Text(pygame.sprite.Sprite):

    def __init__(self, text, fontsize, fontcolor, font, where, should_i_update):
        super().__init__()
        self.level= text
        self.color = fontcolor

        # this tells whether to change hwo the text looks when the mouse pointer hovers over the text

        self.is_update = should_i_update
        self.fontsize = fontsize
        self.font = pygame.font.Font(font, fontsize)
        self.image = self.font.render(text, True, fontcolor)
        self.rect = self.image.get_rect(center = where)
        self.mouse_click_tick = 0

    def mouse_click(self):
        
        # if the mouse pointer collides with the text sprite and the mouse button down is pressed, basically clicking the sprite
        # an event is posted having the text of the text sprite which was clicked

        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.is_update:

            # dims the text when the mouse pointer hovers over the sprite

            self.image = self.font.render(self.level, True, (100,100,100))
            if pygame.mouse.get_pressed()[0] == True and self.mouse_click_tick > 20:
                level_pressed = pygame.USEREVENT + 1
                my_event = pygame.event.Event(level_pressed, message=f"{self.level}")
                pygame.event.post(my_event)
        else:

            # reverts back to the actual color

            self.image = self.font.render(self.level, True, self.color)
        self.mouse_click_tick += 1
        # if self.mouse_click_tick == 20: self.mouse_click_tick = -1
    def update(self):
        return self.mouse_click()
    

def add_text(mainmenu_group, level_group, game_over,settings_group, graphics_group, music_group, sound_group, background_group, how_to_play_group, music_text_group, sound_text_group):

    # adds text for the user interface

    global font 
    font = 'font/minecraft_font.ttf'
    Play = Text("Play", 50, "white", font, (300,300),True)
    Level = Text("Level", 50, "white", font, (300,380),True)
    Settings = Text("Settings", 50, "white", font, (300,460),True)
    HowToPlay = Text("How to play", 50, "white", font, (300,540),True)
    Exit = Text("Exit", 50, "white", font, (320,620),True)
    mainmenu_group.add(Play)
    mainmenu_group.add(Level)
    mainmenu_group.add(Settings)
    mainmenu_group.add(HowToPlay)
    mainmenu_group.add(Exit)

    Easy = Text("Easy", 50, "white", font, (300,320),True)
    Medium = Text("Medium", 50, "white", font, (300,420),True)
    Hard = Text("Hard", 50, "white", font, (300,520),True)
    Back = Text("Back", 50, "white", font, (500,650),True)
    level_group.add(Back)
    level_group.add(Hard)
    level_group.add(Easy)
    level_group.add(Medium)

    Music = Text("Music", 50, "white", font, (300,340),True)
    Sound = Text("Sound", 50, "white", font, (300,420),True)
    Graphics = Text("Graphics", 50, "white", font, (300,500),True)
    Background = Text("Background", 50, "white", font, (300,580),True)
    Back = Text("Back", 50, "white", font, (500,650),True)
    

    settings_group.add(Back)
    settings_group.add(Music)
    settings_group.add(Sound)
    settings_group.add(Graphics)
    settings_group.add(Background)

    Low =  Text("Low", 50, "white", font, (300,380),True)
    Medium = Text("Medium", 50, "white", font, (300,460),True)
    High = Text("High", 50, "white", font, (300,540),True)
    Back = Text("Back", 50, "white", font, (500,650),True)

    graphics_group.add(Back)
    graphics_group.add(Low)
    graphics_group.add(Medium)
    graphics_group.add(High)

    MusicON = Text("Music ON", 50, "white", font, (300,380),True)
    MusicOFF = Text("Music OFF", 50, "white", font, (300,460),True)

     
    music_text_group.add(MusicON)
    music_text_group.add(MusicOFF)
    music_text_group.add(Text("Back", 50, "white", font, (500,650),True))

    SoundON = Text("Sound ON", 50, "white", font, (300,380),True)
    SoundOFF = Text("Sound OFF", 50, "white", font, (300,460),True)

    sound_text_group.add(SoundON)
    sound_text_group.add(SoundOFF)
    sound_text_group.add(Text("Back", 50, "white", font, (500,650),True))

    game_over.add(Text("Back to menu", 40, "white", font, (320,340), True))
    game_over.add(Text("Play again", 40, "white", font, (320,420), True))

# displays the text sprites added earlier

def user_display(screen, welcome_surface, welcome_rect, level_group, mouse_group, phase,game_over, win,player,time_left,added,score_group, menu,mainmenu_group):
    
    # this is before beginning the game

    if phase =='interface':
        if menu == "Level":
            pygame.mouse.set_visible(False)
            screen.fill("black")
            Level = Text("Level", 100, "white", font, (300,150),True)
            screen.blit(Level.image, Level.rect)
            level_group.draw(screen)
            level_group.update()
            mouse_group.draw(screen)
            mouse_group.update(level_group)
        if menu == "main":
            pygame.mouse.set_visible(False)
            screen.fill("black")
            screen.blit(welcome_surface, welcome_rect)
            mainmenu_group.draw(screen)
            mainmenu_group.update()
            mouse_group.draw(screen)
            mouse_group.update(mainmenu_group)

    # this is the game over interface

    elif phase == "end":
        pygame.mouse.set_visible(False)
        screen.fill("black")
        if not(added):
            if win: score_group.add(Text("You win!", 80, "white", font, (320,200), False))
            else: score_group.add(Text("Game over", 80, "white", font, (320,200), False))
            if player.health > 1: player.score += player.time_left * 10
            score_group.add(Text(f"Score: {player.score}", 40, "white", font, (320,570), False))
        game_over.draw(screen)
        game_over.update()
        score_group.draw(screen)
        mouse_group.draw(screen)
        mouse_group.update(game_over)
        time_left = 0
        return time_left, True
    

def display_main(screen, title_surf, title_rect, mainmenu_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    screen.blit(title_surf, title_rect)
    mainmenu_group.draw(screen)
    mainmenu_group.update()
    mouse_group.draw(screen)
    mouse_group.update(mainmenu_group)

def display_level(screen, level_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    Level = Text("Level", 100, "white", font, (300,150),True)
    screen.blit(Level.image, Level.rect)
    level_group.draw(screen)
    level_group.update()
    mouse_group.draw(screen)
    mouse_group.update(level_group)

def display_settings(screen, settings_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    Settings = Text("Settings", 100, "white", font, (300,150),True)
    screen.blit(Settings.image, Settings.rect)
    settings_group.draw(screen)
    settings_group.update()
    mouse_group.draw(screen)
    mouse_group.update(settings_group)

def display_graphics(screen, graphics_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    Graphics = Text("Graphics", 100, "white", font, (300,150),True)
    screen.blit(Graphics.image, Graphics.rect)
    graphics_group.draw(screen)
    graphics_group.update()
    mouse_group.draw(screen)
    mouse_group.update(graphics_group)

def display_end(screen, added, score_group, game_over, win, player, time_left, mouse_group):
        pygame.mouse.set_visible(False)
        screen.fill("black")
        if not(added):
            if win: score_group.add(Text("You win!", 80, "white", font, (320,200), False))
            else: score_group.add(Text("Game over", 80, "white", font, (320,200), False))
            if player.health > 1: player.score += player.time_left * 100
            score_group.add(Text(f"Score: {player.score}", 40, "white", font, (320,570), False))
        game_over.draw(screen)
        game_over.update()
        score_group.draw(screen)
        mouse_group.draw(screen)
        mouse_group.update(game_over)
        time_left = 0
        return time_left, True

def display_music(screen, music_text_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    Music = Text("Music", 100, "white", font, (300,150),True)
    screen.blit(Music.image, Music.rect)
    print(music_text_group)
    music_text_group.draw(screen)
    music_text_group.update()
    mouse_group.draw(screen)
    mouse_group.update(music_text_group)

def display_sound(screen, sound_text_group, mouse_group):
    pygame.mouse.set_visible(False)
    screen.fill("black")
    Sound = Text("Sound", 100, "white", font, (300,150),True)
    screen.blit(Sound.image, Sound.rect)
    sound_text_group.draw(screen)
    sound_text_group.update()
    mouse_group.draw(screen)
    mouse_group.update(sound_text_group)