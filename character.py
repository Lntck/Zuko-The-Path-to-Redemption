import pygame


class Character:
    def __init__(self, x, y, width, height, speed, character_image_path, sprite_path, size):
        self.size = size
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.character_image_path = character_image_path
        self.sprites = sprite_path
        self.character = pygame.Rect((x, y, width, height))
        self.speed = speed
        self.height_y = 0
        self.jump = False
        self.jump_force = 30
        self.attack_type = 0
        self.attacking = False
        self.flip = 0
        self.ball_group = pygame.sprite.Group()
    
    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.character)
    
    def move(self, screen, target):
        gravity = 2
        dx = 0
        dy = 0
        if not self.attacking:
            # movement <- | ->
            if pygame.key.get_pressed()[pygame.K_a]:
                dx = -self.speed
            if pygame.key.get_pressed()[pygame.K_d]:
                dx = self.speed
            # jump 
            if pygame.key.get_pressed()[pygame.K_w] and not self.jump:
                self.height_y = -self.jump_force
                self.jump = True
            # attack
            # hand strike
            if pygame.key.get_pressed()[pygame.K_j]:
                self.attack_type = 1
                self.attack(screen, target)
            # kick leg
            if pygame.key.get_pressed()[pygame.K_k]:
                self.attack_type = 2
                self.attack(screen, target)
            # (fire/water/air) ball
            if pygame.key.get_pressed()[pygame.K_l]:
                self.attack_type = 3
                self.attack(screen, target)
        
        self.height_y += gravity if self.height_y < self.jump_force else 0

        if 0 <= self.character.x + dx <= self.size[0] - self.width:
            self.character.x += dx
        if 0 <= self.character.y + dy <= self.size[1]:
            self.character.y += dy

        if self.y + self.height >= self.character.y + self.height + self.height_y:
            self.character.y += self.height_y

        if self.height_y >= self.jump_force and self.character.y == int(self.size[1] * 0.58):
                self.jump = False
        
        if self.character.x < target.character.x:
            self.flip = 0
        else:
            self.flip = 1
    
    def attack(self, screen, target):
        self.attacking = True
        if self.attack_type == 1:
            strike = pygame.Rect((self.character.x + self.width) - (2 * self.width * self.flip), self.character.y, self.width, self.height // 3)
            pygame.draw.rect(screen, (255, 0, 0), strike)
            if strike.colliderect(target.character):
                print('hit hand strike')
        elif self.attack_type == 2:
            kick = pygame.Rect((self.character.x + self.width) - (2 * self.width * self.flip), self.character.y + self.height * 0.4, self.width, self.height * 0.6)
            pygame.draw.rect(screen, (255, 0, 0), kick)
            if kick.colliderect(target.character):
                print('hit leg kick')
        elif self.attack_type == 3:
            ball = Ball(self.character.x + self.width, self.character.y + self.height // 2, self.flip, pygame.image.load("assets/sprites/fireball.png"), target, self.size)
            self.ball_group.add(ball)
        self.attack_type = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, img, target, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.direction = -1 if direction else 1
        self.target = target
        self.speed = 10
        self.image = pygame.transform.flip(img, direction, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)



    def update(self):
        # move ball
        self.rect.x += (self.direction * self.speed)
        # if ball has gone off screen he died
        if self.rect.right < 0 or self.rect.left > self.size[0]:
            self.kill()
        
        if self.rect.colliderect(self.target.character):
            print("ball HIT")
            self.kill()
