import pygame
import random
import Buttons
from PIL.ImageChops import screen

import settings
from settings import *
from player import Player
from sprites123 import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites


class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Исправлено: передаем кортеж
        pygame.display.set_caption("lol")
        self.clock = pygame.time.Clock()
        self.running = True
        self.w = WINDOW_WIDTH
        self.h = WINDOW_HEIGHT
        self.x = 3
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.can_shoot = True
        self.shoot_time = 100
        self.gun_cooldown = 300
        # audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.3)
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.set_volume(0.2)
        self.music.play(loops=-1)

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1000)
        self.spawn_positions = []

        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_names in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_names)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            print(self.gun.rect.center)
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def setup(self):  # draw map recode
        map = load_pygame(join('data', 'maps', 'world(2).tmx'))
        map2 = load_pygame(join('data', 'maps', 'dungeon.tmx'))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))




    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False,
                                                                pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask)
        if collision_sprites:
            for sprite in collision_sprites:
                sprite.destroy()
                self.x -= 1
        if self.x == 0:
            self.running = False
        print(self.x)

    def health(self):
        if self.x == 3:
            im = pygame.image.load(join('images', 'Hp', 'heart.png'))
            self.display_surface.blit(im, (50, 30))
            self.display_surface.blit(im, (90, 30))
            self.display_surface.blit(im, (130, 30))
        elif self.x == 2:
            im = pygame.image.load(join('images', 'Hp', 'heart.png'))
            self.display_surface.blit(im, (50, 30))
            self.display_surface.blit(im, (90, 30))
        elif self.x == 1:
            im = pygame.image.load(join('images', 'Hp', 'heart.png'))
            self.display_surface.blit(im, (50, 30))

    def dialogs(self):
        pass


    def run(self):

        st_but = Buttons.Button(self.w / 2 - (252 / 2), 150, 252, 74, 'Новая игра', 'menu_assets/1.png', 'music/kn2.mp3')
        sp = [st_but]


        while self.running:
            dt = self.clock.tick(60) / 1000  # Ограничиваем FPS и передаем dt в секундах

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT and event.button == st_but:
                    a = 'dggggggggggggggggggggggggggg'
                    st_but.text_but(a)
                for i in sp:
                    i.hand_ev(event)

                if event.type == self.enemy_event:
                    Enemy(random.choice(self.spawn_positions), random.choice(list(self.enemy_frames.values())),
                          (self.all_sprites, self.enemy_sprites),
                          self.player, self.collision_sprites)

            # update
            self.gun_timer()
            self.all_sprites.update(dt)
            self.input()
            self.bullet_collision()
            self.player_collision()
            # draw
            self.display_surface.fill((0, 0, 0))
            self.display_surface.fill('black')  # Очистка экрана
            self.all_sprites.draw(self.player.rect.center)
            for j in sp:
                j.draw(self.display_surface)
                j.check(pygame.mouse.get_pos())
            self.health()
            pygame.display.flip()  # Используем flip для обновления экрана
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
