import pygame


class Button():
    def __init__(self, x, y, width, height, text, image1, sound_but=None, image_ch=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image1 = pygame.image.load(image1)
        self.image1 = pygame.transform.scale(self.image1, (width, height))
        self.image_ch0 = self.image1
        if image_ch:
            self.image_ch0 = pygame.load(image_ch)
            self.image_ch0 = pygame.transform.scale(self.image.ch0, (width, height))
        self.rect = self.image1.get_rect(topleft=(x, y))
        self.sound = None
        if sound_but:
            self.sound = pygame.mixer.Sound(sound_but)
        self.navig = False

    def draw(self, screen):
        if self.navig:
            im = self.image_ch0
        else:
            im = self.image1
        screen.blit(im, self.rect.topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check(self, mouse_pos):
        self.navig = self.rect.collidepoint(mouse_pos)

    def hand_ev(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.navig:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def text_but(self, text):
        self.text = text
