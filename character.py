import pygame
import random


class Character:
    def __init__(self, x, y, width, height, speed, health, flip, sprite_sheet, ball, animation, sound):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.character = pygame.Rect((x, y, width, height))
        self.animation_list = self.load_images(sprite_sheet, animation)
        self.action = 0
        self.sound_list = sound
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.ball = ball
        self.speed = speed
        self.height_y = 0
        self.jump = False
        self.running = False
        self.jump_force = 30
        self.attack_type = 0
        self.attacking = False
        self.attack_cooldown = 0
        self.hit = False
        self.health = health
        self.alive = True
        self.flip = flip
        self.ball_group = pygame.sprite.Group()

    def load_images(self, sprite_sheet, animation):
        animation_list = list()
        for y, n in enumerate(animation):
            img_list = list()
            for x in range(n):
                img = sprite_sheet.subsurface(x * 128, y * 128, 128, 128)
                img_list.append(pygame.transform.scale(img, (128 * 2, 128 * 2)))
            animation_list.append(img_list)
        return animation_list

    def update(self):
        if self.health <= 0:
            self.alive = False
            self.update_action(7)
        elif self.hit:
            self.update_action(6)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            if self.attack_type == 2:
                self.update_action(4)
            if self.attack_type == 3:
                self.update_action(5)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)
        cooldown = 200
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
            if self.action in (3, 4, 5):
                self.attacking = False
                self.attack_cooldown = 25
            elif self.action == 6:
                self.hit = False
                self.attack_cooldown = 40
                self.attacking = False

    def update_action(self, action):
        if self.action != action:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = 0
            self.action = action

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.character.x - 64, self.character.y - 40))
    
    def move(self, screen, target, size, AI=False):
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        if not AI:
            if not self.attacking and self.alive:
                # movement <- | ->
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.running = True
                    dx = -self.speed
                if pygame.key.get_pressed()[pygame.K_d]:
                    self.running = True
                    dx = self.speed
                # jump
                if pygame.key.get_pressed()[pygame.K_w] and not self.jump:
                    self.height_y = -self.jump_force
                    self.sound_list[0].play()
                    self.jump = True
                # attack
                # hand strike
                if pygame.key.get_pressed()[pygame.K_j]:
                    self.attack_type = 1
                    self.attack(screen, target, size)
                # kick leg
                if pygame.key.get_pressed()[pygame.K_k]:
                    self.attack_type = 2
                    self.attack(screen, target, size)
                # (fire/water/air) ball
                if pygame.key.get_pressed()[pygame.K_l]:
                    self.attack_type = 3
                    self.attack(screen, target, size)
        else:
            if not self.attacking and self.alive:
                # movement <- | ->
                if self.character.x + random.choice((300, 10)) > target.character.x:
                    self.running = True
                    dx = -self.speed
                elif self.character.x - random.choice((300, 10)) < target.character.x:
                    self.running = True
                    dx = self.speed
                # jump
                jump_rand = random.random()
                if jump_rand < 0.01 and not self.jump:
                    self.height_y = -self.jump_force
                    self.sound_list[0].play()
                    self.jump = True
                # attack
                # hand strike
                if target.character.x - 150 < self.character.x < target.character.x + 150 and random.random() > 0.9:
                    self.attack_type = 1
                    self.attack(screen, target, size)
                # kick leg
                elif target.character.x - 50 < self.character.x < target.character.x + 50 and random.random() > 0.1:
                    self.attack_type = 2
                    self.attack(screen, target, size)
                # (fire/water/air) ball
                if random.random() < 0.04:
                    self.attack_type = 3
                    self.attack(screen, target, size)
        
        self.height_y += gravity if self.height_y < self.jump_force else 0

        if 0 <= self.character.x + dx <= size[0] - self.width:
            self.character.x += dx
        if 0 <= self.character.y + dy <= size[1]:
            self.character.y += dy

        if self.y + self.height >= self.character.y + self.height + self.height_y:
            self.character.y += self.height_y

        if self.height_y >= self.jump_force and self.character.y == int(size[1] * 0.58):
                self.jump = False

        self.attack_cooldown = self.attack_cooldown - 1 if self.attack_cooldown > 0 else self.attack_cooldown

        if self.character.x < target.character.x:
            self.flip = False
        else:
            self.flip = True
    
    def attack(self, screen, target, size):
        if not self.attack_cooldown:
            self.attacking = True
            if self.attack_type == 1:
                self.sound_list[1].play()
                strike = pygame.Rect((self.character.x + self.width) - (2 * self.width * self.flip), self.character.y, self.width, self.height // 3)
                # pygame.draw.rect(screen, (255, 0, 0), strike)
                if strike.colliderect(target.character):
                    target.hit = True
                    target.health -= 8
                    print('hit hand strike')
            elif self.attack_type == 2:
                self.sound_list[2].play()
                kick = pygame.Rect((self.character.x + self.width) - (2 * self.width * self.flip), self.character.y + self.height * 0.4, self.width, self.height * 0.6)
                # pygame.draw.rect(screen, (255, 0, 0), kick)
                if kick.colliderect(target.character):
                    target.hit = True
                    target.health -= 9
                    print('hit leg kick')
            elif self.attack_type == 3:
                self.sound_list[-1].play()
                ball = Ball(self.character.x + self.width, self.character.y + self.height // 3.2, self.flip, self.ball, target, size)
                self.ball_group.add(ball)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, flip, img, target, size):
        super(Ball, self).__init__()
        self.size = size
        self.direction = -1 if flip else 1
        self.target = target
        self.speed = 9
        self.img = img
        self.flip = flip
        self.image = pygame.transform.scale(pygame.transform.flip(img[0], flip, False), (64, 64))
        self.update_time = pygame.time.get_ticks()
        self.flag = True
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > self.size[0]:
            self.kill()
        
        if self.rect.colliderect(self.target.character):
            self.target.hit = True
            self.target.health -= 19
            print("ball HIT")
            self.kill()

    def update_animation(self):
        cooldown = 150
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            if self.flag:
                self.image = pygame.transform.scale(pygame.transform.flip(self.img[1], self.flip, False), (64, 64))
                self.flag = False
            else:
                self.image = pygame.transform.scale(pygame.transform.flip(self.img[0], self.flip, False), (64, 64))
                self.flag = True