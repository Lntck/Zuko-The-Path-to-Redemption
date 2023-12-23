import pygame


class Character:
    def __init__(self, x, y, width, height, speed, character_image_path, sprite_path):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.character_image_path = character_image_path
        self.sprites = sprite_path
        self.character = pygame.Rect((x, y, width, height))
        self.speed = speed
        self.height_y = 0
        self.jump = False
        self.jump_force = 30
    
    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.character)
    
    def move(self):
        gravity = 2
        dx = 0
        dy = 0
        
        if pygame.key.get_pressed()[pygame.K_a]:
            dx = -self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            dx = self.speed
        if pygame.key.get_pressed()[pygame.K_w] and not self.jump:
            self.height_y = -self.jump_force
            self.jump = True
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.height_y = -self.jump_force
        
        self.height_y += gravity if self.height_y < self.jump_force else 0

        if 0 <= self.character.x + dx <= 900 - self.width:
            self.character.x += dx
        if 0 <= self.character.y + dy <= 520:
            self.character.y += dy
        if self.y + self.height >= self.character.y + self.height + self.height_y:
            self.character.y += self.height_y

        if self.height_y >= self.jump_force and self.character.y == 300:
                self.jump = False
        