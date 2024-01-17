import pygame
import pygame_menu as pm
from button import Button
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
levels_bg = pygame.transform.scale(pygame.image.load("assets/images/levels.jpeg").convert_alpha(), size)
fightmap1 = pygame.transform.scale(pygame.image.load("assets/images/fightmap1.jpeg").convert_alpha(), size)
fightmap2 = pygame.transform.scale(pygame.image.load("assets/images/fightmap2.jpg").convert_alpha(), size)
credits_bg = pygame.transform.scale(pygame.image.load("assets/images/credits.png").convert_alpha(), size)
window_bg = pygame.transform.scale(pygame.image.load("assets/images/settings.jpg").convert_alpha(), size)

Winner = 0
Hero_health = 100
Target_health = 100

Zuko_sheet = pygame.image.load("assets/sprites/Zuko_1.png").convert_alpha()
Zuko_sheet_2 = pygame.image.load("assets/sprites/Zuko_2.png").convert_alpha()
Zhao_sheet = pygame.image.load("assets/sprites/Zhao.png").convert_alpha()
Aang_sheet = pygame.image.load("assets/sprites/Aang.png").convert_alpha()
fireball = (pygame.image.load("assets/sprites/fireball1.png").convert_alpha(),
            pygame.image.load("assets/sprites/fireball2.png").convert_alpha())
airball = (pygame.image.load("assets/sprites/airball1.png").convert_alpha(),
            pygame.image.load("assets/sprites/airball2.png").convert_alpha())

Zuko_healthbar = pygame.image.load("assets/sprites/Zuko_healthbar.png").convert_alpha()
Zhao_healthbar = pygame.image.load("assets/sprites/Zhao_healthbar.png").convert_alpha()
Zuko_healthbar_2 = pygame.image.load("assets/sprites/Zuko_2_healthbar.png").convert_alpha()
Aang_healthbar = pygame.image.load("assets/sprites/Aang_healthbar.png").convert_alpha()

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
LevelsTheme = pygame.mixer.Sound("assets/music/Levels_theme.mp3")
LevelsTheme.set_volume((0.1 if bool(Music) else 0))
SettingsTheme = pygame.mixer.Sound("assets/music/Settings_theme.mp3")
SettingsTheme.set_volume((0.1 if bool(Music) else 0))
EndTheme = pygame.mixer.Sound("assets/music/End_title_theme.mp3")
EndTheme.set_volume((0.1 if bool(Music) else 0))
Agnikai_fight = pygame.mixer.Sound("assets/music/Agnikai_fight.mp3")
Agnikai_fight.set_volume((0.45 if bool(Music) else 0))
Agnikai_cutscene = pygame.mixer.Sound("assets/music/Agnikai_cutscene.mp3")
Agnikai_cutscene.set_volume((0.45 if bool(Music) else 0))
fight2 = pygame.mixer.Sound("assets/music/fight2.mp3")
fight2.set_volume((0.45 if bool(Music) else 0))
Crossroads_cutscene = pygame.mixer.Sound("assets/music/Crossroads_cutscene.mp3")
Crossroads_cutscene.set_volume((0.45 if bool(Music) else 0))

current_scene = None
current_fight = None


# Scene switching function
def switch_scene(scene):
    global current_scene
    current_scene = scene


def draw_healthbar(health, x, y, img, flip, scale):
    k = health / 100
    pygame.draw.rect(screen, "Green", pygame.Rect(x + (58 if flip else 18), y + 50, (img.get_width() * scale - 75) * k, img.get_height() * scale - 50))
    screen.blit(pygame.transform.scale(pygame.transform.flip(img, flip, False).convert_alpha(), (img.get_width() * scale, img.get_height() * scale)), (x, y))


def draw_video(video, scene, sound, fps_video):
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    img = cv2.transpose(cv2.resize(frame, size))
    surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
    clock2 = pygame.time.Clock()
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
                draw_video("assets/videos/First_agnikai.mp4", fight_scene1, Agnikai_cutscene, fps_video=24)
            if event.type == pygame.USEREVENT and event.button == levels_button:
                running = False
                MainTheme.stop()
                switch_scene(levels_scene)
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


# Scene Levels
def levels_scene():
    first_level = Button(size[0] * 0.13, size[1] * 0.11, 330, 210, "", 36, 'black',
                         "assets/images/first_btn.png", "assets/images/first_btn_active.png",
                         "assets/music/clickbutton.mp3")
    second_level = Button(size[0] * 0.55, size[1] * 0.15, 300, 200, "", 36, 'black',
                         "assets/images/second_btn.png", "assets/images/second_btn_active.png",
                         "assets/music/clickbutton.mp3")
    third_level = Button(size[0] * 0.336, size[1] * 0.54, 300, 200, "", 36, 'black',
                          "assets/images/third_btn.png", "assets/images/third_btn_active.png",
                          "assets/music/clickbutton.mp3")
    LevelsTheme.play(-1)
    running = True
    while running:
        screen.blit(levels_bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                LevelsTheme.stop()
                switch_scene(main_menu)
            if event.type == pygame.USEREVENT and event.button == first_level:
                running = False
                LevelsTheme.stop()
                draw_video("assets/videos/First_agnikai.mp4", fight_scene1, Agnikai_cutscene, fps_video=24)
            if event.type == pygame.USEREVENT and event.button == second_level and len(Levels) > 1:
                running = False
                LevelsTheme.stop()
                draw_video("assets/videos/Crossroads_of_fate.mp4", fight_scene2, Crossroads_cutscene, fps_video=30)
            first_level.handle_event(event)
            second_level.handle_event(event)
            # third_level.handle_event(event)

        first_level.check_hover(pygame.mouse.get_pos())
        first_level.draw(screen)

        second_level.check_hover(pygame.mouse.get_pos())
        second_level.draw(screen)

        third_level.check_hover(pygame.mouse.get_pos())
        third_level.draw(screen)
        pygame.display.flip()


# Scene First Fight
def fight_scene1():
    global Winner, Hero_health, Target_health, current_fight
    current_fight = fight_scene1
    Winner = 0
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

        screen.blit(fightmap1, (0, 0))
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


# Scene Second Fight
def fight_scene2():
    global Winner, Hero_health, Target_health, current_fight
    current_fight = fight_scene2
    Winner = 0
    Hero_health = 100
    Target_health = 100
    fight2.play(-1)
    hero = Character(100, int(size[1] * 0.58), 100, 180, 6, Hero_health, False, Zuko_sheet_2, fireball, ZUKO_ANIMATION,
                     sound_list)
    target = Character(size[0] - 200, int(size[1] * 0.58), 100, 180, 6, Target_health, True, Aang_sheet, airball,
                       ZHAO_ANIMATION, sound_list)
    clock = pygame.time.Clock()
    running = True
    cooldown_death = 100
    while running:
        clock.tick(fps)

        screen.blit(fightmap2, (0, 0))
        draw_healthbar(hero.health, 20, 0, Zuko_healthbar_2, True, 2.5)
        draw_healthbar(target.health, size[0] - 235, 0, Aang_healthbar, False, 2.5)

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
                fight2.stop()
                switch_scene(main_menu)
        hero.update()
        target.update()
        hero.draw(screen)
        target.draw(screen)
        Winner = check_win(hero, target)
        cooldown_death = cooldown_death - 1 if Winner else cooldown_death
        if Winner and not cooldown_death:
            running = False
            fight2.stop()
            Hero_health, Target_health = hero.health, target.health
            switch_scene(winner_scene)
        pygame.display.flip()


def winner_scene():
    global Levels
    Levels = Levels + "2" if len(Levels) == 1 and Winner == 1 else (Levels + "3" if len(Levels) == 2 and Winner == 1 else Levels)
    back_to_menu = Button(size[0] // 2 - window_bg.get_width() * 0.28, size[1] // 1.9, 250, 50, "Back to menu", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    restart = Button(size[0] // 1.98, size[1] // 1.9, 250, 50, "Restart", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    next_level = Button(size[0] // 2 - window_bg.get_width() * 0.14, size[1] // 1.58, 250, 50, "Next level", 20,
                          "black", "assets/images/play_button.png",
                          "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
    running = True
    while running:
        clock.tick(fps)
        screen.blit(pygame.transform.scale(window_bg, (window_bg.get_width() * 0.6, window_bg.get_height() * 0.6)),
                    (size[0] // 2 - window_bg.get_width() * 0.3, size[1] // 2 - window_bg.get_width() * 0.15))
        font = pygame.font.Font("assets/fonts/rubber-biscuit.bold.ttf", 36)
        text = font.render(f"Victory" if Winner == 1 else f"Defeat", True, 'black')
        points = font.render(f"Points/ {Hero_health * 9}", True, 'black')
        screen.blit(text, (size[0] // 2 - window_bg.get_width() * 0.08, size[1] // 2 - window_bg.get_width() * 0.1))
        screen.blit(points, (size[0] // 2 - window_bg.get_width() * 0.13, size[1] // 2 - window_bg.get_width() * 0.05))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                switch_scene(main_menu)
            if event.type == pygame.USEREVENT and event.button == back_to_menu:
                running = False
                switch_scene(main_menu)
            if event.type == pygame.USEREVENT and event.button == restart:
                running = False
                switch_scene(current_fight)
            if event.type == pygame.USEREVENT and event.button == next_level:
                running = False
                if len(Levels) > 1:
                    draw_video("assets/videos/Crossroads_of_fate.mp4", fight_scene2, Crossroads_cutscene, fps_video=30)
                else:
                    switch_scene(main_menu)
            back_to_menu.handle_event(event)
            restart.handle_event(event)
            next_level.handle_event(event)

        back_to_menu.check_hover(pygame.mouse.get_pos())
        back_to_menu.draw(screen)

        restart.check_hover(pygame.mouse.get_pos())
        restart.draw(screen)

        if Winner == 1:
            next_level.check_hover(pygame.mouse.get_pos())
            next_level.draw(screen)
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

    def save():
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

    settings.add.button(title="Apply Settings", action=save)
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

with open("data/data.txt", 'r') as f:
    data = f.read().split("\n")
with open("data/data.txt", 'w+') as f:
    data[-1] = f"Unlocked levels	:	{Levels}"
    f.write("\n".join(data))

pygame.quit()