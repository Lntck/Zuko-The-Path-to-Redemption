import os
import sys
import pygame
import pygame_menu as pm
from tools import Button
from character import Character

pygame.init()

clock = pygame.time.Clock()
fps = 60

data = open("data/data.txt")
Options = {i.split("	:	")[0]: i.split("	:	")[1] for i in data.read().split("\n")}
User, Graphic, Resolution, Music, Sound, Difficulty, Levels = Options.values()
data.close()

size = width, height = tuple(map(int, Resolution.split("x")))
screen = pygame.display.set_mode(size)

menu_bg = pygame.transform.scale(pygame.image.load("assets/images/Main_menu.jpeg").convert_alpha(), size)
fightmap = pygame.transform.scale(pygame.image.load("assets/images/fightmap1.jpeg").convert_alpha(), size)
credits_bg = pygame.transform.scale(pygame.image.load("assets/images/credits.png").convert_alpha(), size)
settings_bg = pygame.transform.scale(pygame.image.load("assets/images/settings.jpg").convert_alpha(), size)

Zuko_sheet = pygame.image.load("assets/sprites/Zuko_1.png").convert_alpha()
Zhao_sheet = pygame.image.load("assets/sprites/Zhao.png").convert_alpha()
fireball = (pygame.image.load("assets/sprites/fireball1.png").convert_alpha(), pygame.image.load("assets/sprites/fireball2.png").convert_alpha())

ZUKO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]
ZHAO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]

current_scene = None
flag = False


# Scene switching function
def switch_scene(scene):
    global current_scene
    current_scene = scene


# Scene Main menu
def main_menu():
    global current_scene
    MainTheme = pygame.mixer.Sound("assets/music/Main_lobby_theme.mp3")
    MainTheme.set_volume((0.1 if bool(Music) else 0))
    MainTheme.play(-1)
    play_button = Button(size[0] - 410, size[1]//14, 395, 86, "Play", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    levels_button = Button(size[0] - 410, size[1]//14 + 85, 395, 86, "Levels", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    settings_button = Button(size[0] - 410, size[1]//14 + 170, 395, 86, "Settings", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    credits_button = Button(size[0] - 410, size[1]//14 + 255, 395, 86, "Credits", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    exit_button = Button(size[0] - 410, size[1]//14 + 340, 395, 86, "Exit", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    running = True
    while running:
        screen.blit(menu_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.USEREVENT and event.button == play_button:
                running = False
                MainTheme.stop()
                switch_scene(fight_scene)
            if event.type == pygame.USEREVENT and event.button == credits_button:
                running = False
                MainTheme.stop()
                switch_scene(Credits_scene)
            if event.type == pygame.USEREVENT and event.button == settings_button:
                running = False
                MainTheme.stop()
                switch_scene(Settings_scene)
            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                current_scene = None
            
            play_button.handle_event(event)
            levels_button.handle_event(event)
            settings_button.handle_event(event)
            credits_button.handle_event(event)
            exit_button.handle_event(event)
        
        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen)
        levels_button.check_hover(pygame.mouse.get_pos())
        levels_button.draw(screen)
        settings_button.check_hover(pygame.mouse.get_pos())
        settings_button.draw(screen)
        credits_button.check_hover(pygame.mouse.get_pos())
        credits_button.draw(screen)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
    
        pygame.display.flip()
        clock.tick(fps)


# Scene fight
def fight_scene():
    hero = Character(100, int(size[1] * 0.58), 100, 180, 6, False, Zuko_sheet, fireball, ZUKO_ANIMATION, "")
    target = Character(size[0] - 200, int(size[1] * 0.58), 100, 180, 6, True, Zhao_sheet, fireball, ZHAO_ANIMATION, "")
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        screen.blit(fightmap, (0, 0))
        hero.move(screen, target, size)
        hero.ball_group.update()
        hero.ball_group.draw(screen)
        # target.move(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                switch_scene(main_menu)
        hero.update()
        target.update()
        hero.draw(screen)
        target.draw(screen)
        pygame.display.flip()


# Scene credits
def Credits_scene():
    EndTheme = pygame.mixer.Sound("assets/music/End_title_theme.mp3")
    EndTheme.set_volume((0.1 if bool(Music) else 0))
    EndTheme.play(-1)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        screen.blit(credits_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                EndTheme.stop()
                switch_scene(main_menu)
        pygame.display.flip()


# Scene settings
def Settings_scene():
    global flag
    flag = False

    def main_background() -> None:
        background_image.draw(screen)

    def SaveSettings():
        with open("data/data.txt", 'w+') as f:
            settingsData = settings.get_input_data()
            s = "\n".join([f"{key}\t:\t{(settingsData[key][0][0] if type(settingsData[key]) == tuple else settingsData[key])}" for key in settingsData.keys()])
            s += f"\nUnlocked levels	:	{Levels}"
            f.write(s)

    def disable() -> None:
        global flag
        flag = True
        settings.disable()

    EndTheme = pygame.mixer.Sound("assets/music/Settings_theme.mp3")
    EndTheme.set_volume((0.1 if bool(Music) else 0))
    EndTheme.play(-1)
    clock = pygame.time.Clock()
    running = True

    graphics = [("Low", "low"),
                ("Medium", "medium"),
                ("High", "high")]
    resolution = [("900x500", "900x500"),
                  ("1280x720", "1280x720"),
                  ("1600x900", "1600x900"),
                  ("1920x1080", "1920x1080")]
    difficulty = [("Easy", "Easy"),
                  ("Medium", "Medium"),
                  ("Hard", "Hard")]

    background_image = pm.BaseImage(image_path=pm.baseimage.IMAGE_EXAMPLE_WALLPAPER)
    theme_bg_image = pm.themes.THEME_ORANGE.copy()
    theme_bg_image.background_color = pm.BaseImage(image_path="assets/images/settings.jpg")
    theme_bg_image.widget_font = pygame.font.Font("assets/fonts/rubber-biscuit.bold.ttf", 30)
    theme_bg_image.title_bar_style = pm.widgets.MENUBAR_STYLE_NONE
    settings = pm.Menu(title="", width=size[0], height=size[1], theme=theme_bg_image)
    settings.add.text_input(title="User Name / ", textinput_id="username", default=User)
    settings.add.dropselect(title="Graphics Level", items=graphics, dropselect_id="graphics level", default="LMH".index(Graphic[0]))
    settings.add.dropselect(title="Window Resolution", items=resolution, dropselect_id="Resolution", default="90121619".index(Resolution[:2])//2)

    settings.add.toggle_switch(title="Music", default=bool(Music), toggleswitch_id="music")
    settings.add.toggle_switch(title="Sounds", default=bool(Sound), toggleswitch_id="sound")

    settings.add.selector(title="Difficulty\t", items=difficulty, selector_id="difficulty", default="EMH".index(Difficulty[0]))

    settings.add.button(title="Apply Settings", action=SaveSettings)
    settings.add.button(title="Reset Settings", action=settings.reset_value)

    settings.add.button(title="Return To Main Menu", action=disable, align=pm.locals.ALIGN_CENTER)

    while running:
        clock.tick(fps)
        screen.blit(settings_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                EndTheme.stop()
                switch_scene(main_menu)
        if settings.is_enabled():
            settings.mainloop(screen, main_background)
        if not settings.is_enabled() and flag:
            running = False
            EndTheme.stop()
            switch_scene(main_menu)
        pygame.display.flip()


# Start
switch_scene(main_menu)
while current_scene is not None:
    current_scene()
pygame.quit()