import os
import sys
import pygame
from tools import Button
from character import Character

pygame.init()
fps = 60
menu_bg = pygame.image.load("images/Main_menu.jpeg")
fightmap = pygame.image.load("images/fightmap1.jpeg")
credits = pygame.image.load("images/credits.png")
size = width, height = 900, 520
screen = pygame.display.set_mode(size)
current_scene = None


# Scene switching function
def switch_scene(scene):
    global current_scene
    current_scene = scene


# Scene Main menu
def main_menu():
    global current_scene
    MainTheme = pygame.mixer.Sound("music/Main_lobby_theme.mp3")
    MainTheme.set_volume(0.1)
    MainTheme.play(-1)
    play_button = Button(490, 35, 395, 86, "Play", "images/play_button.png", "images/activeplay_button.png", "music/clickbutton.mp3")
    levels_button = Button(490, 120, 395, 86, "Levels", "images/play_button.png", "images/activeplay_button.png", "music/clickbutton.mp3")
    settings_button = Button(490, 205, 395, 86, "Settings", "images/play_button.png", "images/activeplay_button.png", "music/clickbutton.mp3")
    credits_button = Button(490, 290, 395, 86, "Credits", "images/play_button.png", "images/activeplay_button.png", "music/clickbutton.mp3")
    exit_button = Button(490, 375, 395, 86, "Exit", "images/play_button.png", "images/activeplay_button.png", "music/clickbutton.mp3")
    clock = pygame.time.Clock()
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
    hero = Character(180, 300, 100, 180, 6, "asdasd", "asdasd")
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        hero.move()
        screen.blit(fightmap, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                switch_scene(main_menu)
        hero.draw(screen)
        pygame.display.flip()

# Scene credits
def Credits_scene():
    EndTheme = pygame.mixer.Sound("music/End_title_theme.mp3")
    EndTheme.set_volume(0.1)
    EndTheme.play(-1)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        screen.blit(credits, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                EndTheme.stop()
                switch_scene(main_menu)
        pygame.display.flip()


# Start
switch_scene(main_menu)
while current_scene is not None:
    current_scene()
pygame.quit()