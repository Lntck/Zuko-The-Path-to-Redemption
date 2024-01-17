import pygame
import pygame_menu as pm
from button import Button
from character import Character
from video import Video


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60

        with open("data/data.txt") as f:
            options = {i.split("	:	")[0]: i.split("	:	")[1] for i in f.read().split("\n")}

        self.User, self.Graphic, self.Resolution, self.Music, self.Sound, self.Difficulty, self.Levels = options.values()

        self.size = tuple(map(int, self.Resolution.split("x")))
        self.screen = pygame.display.set_mode(self.size)

        self.menu_bg = pygame.transform.scale(pygame.image.load("assets/images/Main_menu.jpeg").convert_alpha(), self.size)
        self.levels_bg = pygame.transform.scale(pygame.image.load("assets/images/levels.jpeg").convert_alpha(), self.size)
        self.fightmap1 = pygame.transform.scale(pygame.image.load("assets/images/fightmap1.jpeg").convert_alpha(), self.size)
        self.fightmap2 = pygame.transform.scale(pygame.image.load("assets/images/fightmap2.jpg").convert_alpha(), self.size)
        self.credits_bg = pygame.transform.scale(pygame.image.load("assets/images/credits.png").convert_alpha(), self.size)
        self.window_bg = pygame.transform.scale(pygame.image.load("assets/images/settings.jpg").convert_alpha(), self.size)

        self.Winner = 0
        self.Hero_health = 100
        self.Target_health = 100

        self.Zuko_sheet = pygame.image.load("assets/sprites/Zuko_1.png").convert_alpha()
        self.Zuko_sheet_2 = pygame.image.load("assets/sprites/Zuko_2.png").convert_alpha()
        self.Zhao_sheet = pygame.image.load("assets/sprites/Zhao.png").convert_alpha()
        self.Aang_sheet = pygame.image.load("assets/sprites/Aang.png").convert_alpha()
        self.fireball = (pygame.image.load("assets/sprites/fireball1.png").convert_alpha(), pygame.image.load("assets/sprites/fireball2.png").convert_alpha())
        self.airball = (pygame.image.load("assets/sprites/airball1.png").convert_alpha(), pygame.image.load("assets/sprites/airball2.png").convert_alpha())

        self.Zuko_healthbar = pygame.image.load("assets/sprites/Zuko_healthbar.png").convert_alpha()
        self.Zhao_healthbar = pygame.image.load("assets/sprites/Zhao_healthbar.png").convert_alpha()
        self.Zuko_healthbar_2 = pygame.image.load("assets/sprites/Zuko_2_healthbar.png").convert_alpha()
        self.Aang_healthbar = pygame.image.load("assets/sprites/Aang_healthbar.png").convert_alpha()

        self.ZUKO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]
        self.ZHAO_ANIMATION = [2, 2, 1, 2, 2, 3, 1, 2]

        fireball_fx = pygame.mixer.Sound("assets/music/fireball_fx.mp3")
        hand_fx = pygame.mixer.Sound("assets/music/hand_fx.mp3")
        leg_fx = pygame.mixer.Sound("assets/music/leg_fx.mp3")
        jump_fx = pygame.mixer.Sound("assets/music/jump_fx.mp3")
        jump_fx.set_volume(0.2)

        self.sound_list = [jump_fx, hand_fx, leg_fx, fireball_fx]

        self.MainTheme = pygame.mixer.Sound("assets/music/Main_lobby_theme.mp3")
        self.MainTheme.set_volume((0.1 if bool(self.Music) else 0))
        self.LevelsTheme = pygame.mixer.Sound("assets/music/Levels_theme.mp3")
        self.LevelsTheme.set_volume((0.1 if bool(self.Music) else 0))
        self.SettingsTheme = pygame.mixer.Sound("assets/music/Settings_theme.mp3")
        self.SettingsTheme.set_volume((0.1 if bool(self.Music) else 0))
        self.EndTheme = pygame.mixer.Sound("assets/music/End_title_theme.mp3")
        self.EndTheme.set_volume((0.1 if bool(self.Music) else 0))
        self.Agnikai_fight = pygame.mixer.Sound("assets/music/Agnikai_fight.mp3")
        self.Agnikai_fight.set_volume((0.45 if bool(self.Music) else 0))
        self.fight2 = pygame.mixer.Sound("assets/music/fight2.mp3")
        self.fight2.set_volume((0.45 if bool(self.Music) else 0))
        agnikai_cutscene_sound = pygame.mixer.Sound("assets/music/Agnikai_cutscene.mp3")
        agnikai_cutscene_sound.set_volume((0.45 if bool(self.Music) else 0))
        crossroads_cutscene_sound = pygame.mixer.Sound("assets/music/Crossroads_cutscene.mp3")
        crossroads_cutscene_sound.set_volume((0.45 if bool(self.Music) else 0))

        self.Cutscene_1 = Video("assets/videos/First_agnikai.mp4", agnikai_cutscene_sound, 24, self.screen, self.size)
        self.Cutscene_2 = Video("assets/videos/Crossroads_of_fate.mp4", crossroads_cutscene_sound, 30, self.screen, self.size)

        self.current_scene = None
        self.current_fight = None
        self.flag = False

    # Scene switching function
    def switch_scene(self, scene):
        self.current_scene = scene

    # Health bar draw
    def draw_healthbar(self, health, x, y, img, flip, scale):
        pygame.draw.rect(self.screen, "Green", pygame.Rect(x + (58 if flip else 18), y + 50, (img.get_width() * scale - 75) * health / 100, img.get_height() * scale - 50))
        self.screen.blit(pygame.transform.scale(pygame.transform.flip(img, flip, False).convert_alpha(), (img.get_width() * scale, img.get_height() * scale)), (x, y))

    # Winner check
    def check_win(self, hero, target):
        return 1 if target.health <= 0 else (2 if hero.health <= 0 else 0)

    # Scene Main menu
    def main_menu(self):
        self.MainTheme.play(-1)

        play_button = Button(self.size[0] - 410, self.size[1]//14, 395, 86, "Play", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        levels_button = Button(self.size[0] - 410, self.size[1]//14 + 85, 395, 86, "Levels", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        settings_button = Button(self.size[0] - 410, self.size[1]//14 + 170, 395, 86, "Settings", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        credits_button = Button(self.size[0] - 410, self.size[1]//14 + 255, 395, 86, "Credits", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        exit_button = Button(self.size[0] - 410, self.size[1]//14 + 340, 395, 86, "Exit", 36, (170, 0, 0), "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")

        running = True
        while running:
            self.screen.blit(self.menu_bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.USEREVENT and event.button == play_button:
                    running = False
                    self.MainTheme.stop()
                    self.Cutscene_1.play()
                    self.switch_scene(self.fight_scene1)
                if event.type == pygame.USEREVENT and event.button == levels_button:
                    running = False
                    self.MainTheme.stop()
                    self.switch_scene(self.levels_scene)
                if event.type == pygame.USEREVENT and event.button == credits_button:
                    running = False
                    self.MainTheme.stop()
                    self.switch_scene(self.credits_scene)
                if event.type == pygame.USEREVENT and event.button == settings_button:
                    running = False
                    self.MainTheme.stop()
                    self.switch_scene(self.settings_scene)
                if event.type == pygame.USEREVENT and event.button == exit_button:
                    running = False
                    self.current_scene = None

                play_button.handle_event(event)
                levels_button.handle_event(event)
                settings_button.handle_event(event)
                credits_button.handle_event(event)
                exit_button.handle_event(event)

            play_button.check_hover(pygame.mouse.get_pos())
            play_button.draw(self.screen)
            levels_button.check_hover(pygame.mouse.get_pos())
            levels_button.draw(self.screen)
            settings_button.check_hover(pygame.mouse.get_pos())
            settings_button.draw(self.screen)
            credits_button.check_hover(pygame.mouse.get_pos())
            credits_button.draw(self.screen)
            exit_button.check_hover(pygame.mouse.get_pos())
            exit_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

    # Scene Levels
    def levels_scene(self):
        first_level = Button(self.size[0] * 0.13, self.size[1] * 0.11, 330, 210, "", 36, 'black', "assets/images/first_btn.png", "assets/images/first_btn_active.png", "assets/music/clickbutton.mp3")
        second_level = Button(self.size[0] * 0.55, self.size[1] * 0.15, 300, 200, "", 36, 'black', "assets/images/second_btn.png", "assets/images/second_btn_active.png", "assets/music/clickbutton.mp3")
        third_level = Button(self.size[0] * 0.336, self.size[1] * 0.54, 300, 200, "", 36, 'black', "assets/images/third_btn.png", "assets/images/third_btn_active.png", "assets/music/clickbutton.mp3")
        self.LevelsTheme.play(-1)
        running = True
        while running:
            self.screen.blit(self.levels_bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.LevelsTheme.stop()
                    self.switch_scene(self.main_menu)
                if event.type == pygame.USEREVENT and event.button == first_level:
                    running = False
                    self.LevelsTheme.stop()
                    self.Cutscene_1.play()
                    self.switch_scene(self.fight_scene1)
                if event.type == pygame.USEREVENT and event.button == second_level and len(self.Levels) > 1:
                    running = False
                    self.LevelsTheme.stop()
                    self.Cutscene_2.play()
                    self.switch_scene(self.fight_scene2)
                first_level.handle_event(event)
                second_level.handle_event(event)
                # third_level.handle_event(event)

            first_level.check_hover(pygame.mouse.get_pos())
            first_level.draw(self.screen)

            second_level.check_hover(pygame.mouse.get_pos())
            second_level.draw(self.screen)

            third_level.check_hover(pygame.mouse.get_pos())
            third_level.draw(self.screen)
            pygame.display.flip()

    # Scene First Fight
    def fight_scene1(self):
        self.Agnikai_fight.play(-1)
        self.current_fight = self.fight_scene1
        self.Winner = 0
        self.Hero_health = 100
        self.Target_health = 100
        hero = Character(100, int(self.size[1] * 0.58), 100, 180, 6, self.Hero_health, False, self.Zuko_sheet, self.fireball, self.ZUKO_ANIMATION,
                         self.sound_list)
        target = Character(self.size[0] - 200, int(self.size[1] * 0.58), 100, 180, 6, self.Target_health, True, self.Zhao_sheet, self.fireball,
                           self.ZHAO_ANIMATION, self.sound_list)
        clock = pygame.time.Clock()
        running = True
        cooldown_death = 100
        while running:
            clock.tick(self.fps)

            self.screen.blit(self.fightmap1, (0, 0))
            self.draw_healthbar(hero.health, 20, 0, self.Zuko_healthbar, True, 2.5)
            self.draw_healthbar(target.health, self.size[0] - 235, 0, self.Zhao_healthbar, False, 2.5)

            hero.move(target, self.size)
            hero.ball_group.update()
            hero.ball_group.draw(self.screen)
            target.move(hero, self.size, AI=True)
            target.ball_group.update()
            target.ball_group.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.Agnikai_fight.stop()
                    self.switch_scene(self.main_menu)
            hero.update()
            target.update()
            hero.draw(self.screen)
            target.draw(self.screen)
            self.Winner = self.check_win(hero, target)
            cooldown_death = cooldown_death - 1 if self.Winner else cooldown_death
            if self.Winner and not cooldown_death:
                running = False
                self.Agnikai_fight.stop()
                self.Hero_health, self.Target_health = hero.health, target.health
                self.switch_scene(self.winner_scene)
            pygame.display.flip()

    # Scene Second Fight
    def fight_scene2(self):
        self.current_fight = self.fight_scene2
        self.Winner = 0
        self.Hero_health = 100
        self.Target_health = 100
        self.fight2.play(-1)
        hero = Character(100, int(self.size[1] * 0.58), 100, 180, 6, self.Hero_health, False, self.Zuko_sheet_2, self.fireball, self.ZUKO_ANIMATION,
                         self.sound_list)
        target = Character(self.size[0] - 200, int(self.size[1] * 0.58), 100, 180, 6, self.Target_health, True, self.Aang_sheet, self.airball,
                           self.ZHAO_ANIMATION, self.sound_list)
        clock = pygame.time.Clock()
        running = True
        cooldown_death = 100
        while running:
            clock.tick(self.fps)
            self.screen.blit(self.fightmap2, (0, 0))
            self.draw_healthbar(hero.health, 20, 0, self.Zuko_healthbar_2, True, 2.5)
            self.draw_healthbar(target.health, self.size[0] - 235, 0, self.Aang_healthbar, False, 2.5)

            hero.move(target, self.size)
            hero.ball_group.update()
            hero.ball_group.draw(self.screen)
            target.move(hero, self.size, AI=True)
            target.ball_group.update()
            target.ball_group.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.fight2.stop()
                    self.switch_scene(self.main_menu)
            hero.update()
            target.update()
            hero.draw(self.screen)
            target.draw(self.screen)
            self.Winner = self.check_win(hero, target)
            cooldown_death = cooldown_death - 1 if self.Winner else cooldown_death
            if self.Winner and not cooldown_death:
                running = False
                self.fight2.stop()
                self.Hero_health, self.Target_health = hero.health, target.health
                self.switch_scene(self.winner_scene)
            pygame.display.flip()

    # Window after fight
    def winner_scene(self):
        self.Levels = self.Levels + "2" if len(self.Levels) == 1 and self.Winner == 1 else (self.Levels + "3" if len(self.Levels) == 2 and self.Winner == 1 else self.Levels)
        back_to_menu = Button(self.size[0] // 2 - self.window_bg.get_width() * 0.28, self.size[1] // 1.9, 250, 50, "Back to menu", 20, "black", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        restart = Button(self.size[0] // 1.98, self.size[1] // 1.9, 250, 50, "Restart", 20, "black", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        next_level = Button(self.size[0] // 2 - self.window_bg.get_width() * 0.14, self.size[1] // 1.58, 250, 50, "Next level", 20, "black", "assets/images/play_button.png", "assets/images/activeplay_button.png", "assets/music/clickbutton.mp3")
        running = True
        while running:
            self.clock.tick(self.fps)
            self.screen.blit(pygame.transform.scale(self.window_bg, (self.window_bg.get_width() * 0.6, self.window_bg.get_height() * 0.6)), (self.size[0] // 2 - self.window_bg.get_width() * 0.3, self.size[1] // 2 - self.window_bg.get_width() * 0.15))

            font = pygame.font.Font("assets/fonts/rubber-biscuit.bold.ttf", 36)
            text = font.render(f"Victory" if self.Winner == 1 else f"Defeat", True, 'black')
            points = font.render(f"Points/ {self.Hero_health * 9}", True, 'black')

            self.screen.blit(text, (self.size[0] // 2 - self.window_bg.get_width() * 0.08, self.size[1] // 2 - self.window_bg.get_width() * 0.1))
            self.screen.blit(points, (self.size[0] // 2 - self.window_bg.get_width() * 0.13, self.size[1] // 2 - self.window_bg.get_width() * 0.05))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.switch_scene(self.main_menu)
                if event.type == pygame.USEREVENT and event.button == back_to_menu:
                    running = False
                    self.switch_scene(self.main_menu)
                if event.type == pygame.USEREVENT and event.button == restart:
                    running = False
                    self.switch_scene(self.current_fight)
                if event.type == pygame.USEREVENT and event.button == next_level:
                    running = False
                    if len(self.Levels) > 1:
                        self.Cutscene_2.play()
                        self.switch_scene(self.fight_scene2)
                    else:
                        self.switch_scene(self.main_menu)
                back_to_menu.handle_event(event)
                restart.handle_event(event)
                next_level.handle_event(event)

            back_to_menu.check_hover(pygame.mouse.get_pos())
            back_to_menu.draw(self.screen)

            restart.check_hover(pygame.mouse.get_pos())
            restart.draw(self.screen)

            if self.Winner == 1:
                next_level.check_hover(pygame.mouse.get_pos())
                next_level.draw(self.screen)
            pygame.display.flip()

    # Scene credits
    def credits_scene(self):
        self.EndTheme.play(-1)
        running = True
        while running:
            self.screen.blit(self.credits_bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.switch_scene(None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    self.EndTheme.stop()
                    self.switch_scene(self.main_menu)
            pygame.display.flip()

    # Scene settings
    def settings_scene(self):
        self.flag = False

        def main_background() -> None:
            background_image.draw(self.screen)

        def save():
            with open("data/data.txt", 'w+') as f:
                settings_data = settings.get_input_data()
                s = "\n".join([f"{key}\t:\t{(settings_data[key][0][0] if isinstance(settings_data[key], tuple) else settings_data[key])}" for key in settings_data.keys()])
                s += f"\nUnlocked levels	:	{self.Levels}"
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
        settings = pm.Menu(title="", width=self.size[0], height=self.size[1], theme=theme_bg_image)
        settings.add.text_input(title="User Name / ", textinput_id="username", default=self.User)
        settings.add.dropselect(title="Graphics Level", items=graphics, dropselect_id="graphics level", default="LMH".index(self.Graphic[0]))
        settings.add.dropselect(title="Window Resolution", items=resolution, dropselect_id="Resolution", default="90121619".index(self.Resolution[:2])//2)

        settings.add.toggle_switch(title="Music", default=bool(self.Music), toggleswitch_id="music")
        settings.add.toggle_switch(title="Sounds", default=bool(self.Sound), toggleswitch_id="sound")

        settings.add.selector(title="Difficulty\t", items=difficulty, selector_id="difficulty", default="EMH".index(self.Difficulty[0]))

        settings.add.button(title="Apply Settings", action=save)
        settings.add.button(title="Reset Settings", action=settings.reset_value)

        settings.add.button(title="Return To Main Menu", action=disable, align=pm.locals.ALIGN_CENTER)

        self.SettingsTheme.play(-1)
        settings.mainloop(self.screen, main_background)
        self.SettingsTheme.stop()
        self.switch_scene(self.main_menu)

    # I wonder what this function does? Exactly START A GAME
    def start_game(self):
        # Start
        self.switch_scene(self.main_menu)
        while self.current_scene is not None:
            self.current_scene()
        # Save data before close
        with open("data/data.txt", 'r') as f:
            data = f.read().split("\n")
        with open("data/data.txt", 'w+') as f:
            data[-1] = f"Unlocked levels	:	{self.Levels}"
            f.write("\n".join(data))
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.start_game()
