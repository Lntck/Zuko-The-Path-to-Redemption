import pygame
import pygame_menu as pm
from tools import Button
from character import Character
import cv2

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
window_bg = pygame.transform.scale(pygame.image.load("assets/images/settings.jpg").convert_alpha(), size)

Winner = 0
Hero_health = 100
Target_health = 100

Zuko_sheet = pygame.image.load("assets/sprites/Zuko_1.png").convert_alpha()
Zhao_sheet = pygame.image.load("assets/sprites/Zhao.png").convert_alpha()
fireball = (pygame.image.load("assets/sprites/fireball1.png").convert_alpha(),
            pygame.image.load("assets/sprites/fireball2.png").convert_alpha())

Zuko_healthbar = pygame.image.load("assets/sprites/Zuko_healthbar.png").convert_alpha()
Zhao_healthbar = pygame.image.load("assets/sprites/Zhao_healthbar.png").convert_alpha()

ZUKO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]
ZHAO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]

fireball_fx = pygame.mixer.Sound("assets/music/fireball_fx.mp3")
hand_fx = pygame.mixer.Sound("assets/music/hand_fx.mp3")
leg_fx = pygame.mixer.Sound("assets/music/leg_fx.mp3")
jump_fx = pygame.mixer.Sound("assets/music/jump_fx.mp3")
jump_fx.set_volume(0.2)

sound_list = [jump_fx, hand_fx, leg_fx, fireball_fx]

MainTheme = pygame.mixer.Sound("assets/music/Main_lobby_theme.mp3")
MainTheme.set_volume((0.1 if bool(Music) else 0))
SettingsTheme = pygame.mixer.Sound("assets/music/Settings_theme.mp3")
SettingsTheme.set_volume((0.1 if bool(Music) else 0))
EndTheme = pygame.mixer.Sound("assets/music/End_title_theme.mp3")
EndTheme.set_volume((0.1 if bool(Music) else 0))
Agnikai_fight = pygame.mixer.Sound("assets/music/Agnikai_fight.mp3")
Agnikai_fight.set_volume((0.45 if bool(Music) else 0))
Agnikai_cutscene = pygame.mixer.Sound("assets/music/Agnikai_cutscene.mp3")
Agnikai_cutscene.set_volume((0.45 if bool(Music) else 0))

current_scene = None


# Scene switching function
def switch_scene(scene):
    global current_scene
    current_scene = scene


def draw_healthbar(health, x, y, img, flip, scale):
    k = health / 100
    pygame.draw.rect(screen, "Green", pygame.Rect(x + (58 if flip else 18), y + 50, (img.get_width() * scale - 75) * k, img.get_height() * scale - 50))
    screen.blit(pygame.transform.scale(pygame.transform.flip(img, flip, False).convert_alpha(), (img.get_width() * scale, img.get_height() * scale)), (x, y))


def draw_video(video, scene, sound):
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    img = cv2.transpose(cv2.resize(frame, size))
    surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
    clock2 = pygame.time.Clock()
    fps_video = 24
    sound.play()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                sound.stop()
                switch_scene(scene)
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(cv2.transpose(cv2.resize(frame, size)), cv2.COLOR_BGR2RGB)
        pygame.surfarray.blit_array(surface, img)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        clock2.tick(fps_video)
    switch_scene(scene)


def check_win(hero, target):
    if target.health <= 0:
        return 1
    elif hero.health <= 0:
        return 2
    return 0


# Scene Main menu
def main_menu():
    global current_scene
    MainTheme.play(-1)
    play_button = Button(size[0] - 410, size[1]//14, 395, 86, "Play", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    levels_button = Button(size[0] - 410, size[1]//14 + 85, 395, 86, "Levels", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    settings_button = Button(size[0] - 410, size[1]//14 + 170, 395, 86, "Settings", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    credits_button = Button(size[0] - 410, size[1]//14 + 255, 395, 86, "Credits", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    exit_button = Button(size[0] - 410, size[1]//14 + 340, 395, 86, "Exit", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
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
                draw_video("assets/videos/First_agnikai.mp4", fight_scene, Agnikai_cutscene)
            if event.type == pygame.USEREVENT and event.button == credits_button:
                running = False
                MainTheme.stop()
                switch_scene(credits_scene)
            if event.type == pygame.USEREVENT and event.button == settings_button:
                running = False
                MainTheme.stop()
                switch_scene(settings_scene)
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
    global Winner, Hero_health, Target_health
    Hero_health = 100
    Target_health = 100
    Agnikai_fight.play(-1)
    hero = Character(100, int(size[1] * 0.58), 100, 180, 6, Hero_health, False, Zuko_sheet, fireball, ZUKO_ANIMATION,
                     sound_list)
    target = Character(size[0] - 200, int(size[1] * 0.58), 100, 180, 6, Target_health, True, Zhao_sheet, fireball,
                       ZHAO_ANIMATION, sound_list)
    clock = pygame.time.Clock()
    running = True
    cooldown_death = 100
    while running:
        clock.tick(fps)

        screen.blit(fightmap, (0, 0))
        draw_healthbar(hero.health, 20, 0, Zuko_healthbar, True, 2.5)
        draw_healthbar(target.health, size[0] - 235, 0, Zhao_healthbar, False, 2.5)

        hero.move(screen, target, size)
        hero.ball_group.update()
        hero.ball_group.draw(screen)
        target.move(screen, hero, size, AI=True)
        target.ball_group.update()
        target.ball_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                Agnikai_fight.stop()
                switch_scene(main_menu)
        hero.update()
        target.update()
        hero.draw(screen)
        target.draw(screen)
        Winner = check_win(hero, target)
        cooldown_death = cooldown_death - 1 if Winner else cooldown_death
        if Winner and not cooldown_death:
            running = False
            Agnikai_fight.stop()
            Hero_health, Target_health = hero.health, target.health
            switch_scene(winner_scene)
        pygame.display.flip()


def winner_scene():
    Back_to_menu = Button(size[0] // 2 - window_bg.get_width() * 0.28, size[1] // 1.9, 250, 50, "Back to menu", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    Restart = Button(size[0] // 1.98, size[1] // 1.9, 250, 50, "Restart", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    Next_level = Button(size[0] // 2 - window_bg.get_width() * 0.14, size[1] // 1.58, 250, 50, "Next level", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    running = True
    while running:
        clock.tick(fps)
        screen.blit(pygame.transform.scale(window_bg, (window_bg.get_width() * 0.6, window_bg.get_height() * 0.6)),
                    (size[0] // 2 - window_bg.get_width() * 0.3, size[1] // 2 - window_bg.get_width() * 0.15))
        font = pygame.font.Font("assets/fonts/rubber-biscuit.bold.ttf", 36)
        text = font.render(f"Victory" if Winner == 1 else f"Defeat", True, 'black')
        Points = font.render(f"Points/ {Hero_health * 9}", True, 'black')
        screen.blit(text, (size[0] // 2 - window_bg.get_width() * 0.08, size[1] // 2 - window_bg.get_width() * 0.1))
        screen.blit(Points, (size[0] // 2 - window_bg.get_width() * 0.13, size[1] // 2 - window_bg.get_width() * 0.05))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                switch_scene(main_menu)
            if event.type == pygame.USEREVENT and event.button == Back_to_menu:
                running = False
                switch_scene(main_menu)
            if event.type == pygame.USEREVENT and event.button == Restart:
                running = False
                switch_scene(fight_scene)
            Back_to_menu.handle_event(event)
            Restart.handle_event(event)
            Next_level.handle_event(event)

        Back_to_menu.check_hover(pygame.mouse.get_pos())
        Back_to_menu.draw(screen)

        Restart.check_hover(pygame.mouse.get_pos())
        Restart.draw(screen)

        if Winner == 1:
            Next_level.check_hover(pygame.mouse.get_pos())
            Next_level.draw(screen)
        pygame.display.flip()


# Scene credits
def credits_scene():
    EndTheme.play(-1)
    running = True
    while running:
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
def settings_scene():
    global flag
    flag = False

    def main_background() -> None:
        background_image.draw(screen)

    def SaveSettings():
        with open("data/data.txt", 'w+') as f:
            settings_data = settings.get_input_data()
            s = "\n".join([f"{key}\t:\t{(settings_data[key][0][0] if type(settings_data[key]) == tuple else settings_data[key])}" for key in settings_data.keys()])
            s += f"\nUnlocked levels	:	{Levels}"
            f.write(s)

    def disable() -> None:
        settings.disable()

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

    SettingsTheme.play(-1)
    settings.mainloop(screen, main_background)
    SettingsTheme.stop()
    switch_scene(main_menu)


# Start
switch_scene(main_menu)
while current_scene is not None:
    current_scene()
pygame.quit()