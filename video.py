import cv2
import pygame


class Video:
    def __init__(self, video, sound, fps_video, screen, size):
        self.cap = cv2.VideoCapture(video)
        self.sound = sound
        self.fps_video = fps_video
        self.size = size
        self.screen = screen

    def play(self):
        ret, frame = self.cap.read()
        img = cv2.transpose(cv2.resize(frame, self.size))
        surface = pygame.surface.Surface((img.shape[0], img.shape[1]))
        clock2 = pygame.time.Clock()
        self.sound.play()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    self.sound.stop()
                    break
            ret, frame = self.cap.read()
            if not ret:
                break
            img = cv2.cvtColor(cv2.transpose(cv2.resize(frame, self.size)), cv2.COLOR_BGR2RGB)
            pygame.surfarray.blit_array(surface, img)
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()
            clock2.tick(self.fps_video)
