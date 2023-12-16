import pygame


class Character:
    def __init__(self, x, y, width, height, speed, character_image_path, sprite_path):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.character_image_path = character_image_path
        self.sprites = sprite_path
        self.character = pygame.Rect((x, y, width, height))
        self.speed = speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.character)
    
    def move(self):
        dx = 0
        dy = 0
        
        if pygame.key.get_pressed()[pygame.K_a]:
            dx = -self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            dx = self.speed
        if pygame.key.get_pressed()[pygame.K_w]:
            dy = -self.speed
        
        self.character.x += dx
        self.character.y += dy
        