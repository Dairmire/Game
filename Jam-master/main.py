import pygame
import random
import settings
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites


def play():
    class Game():
        def __init__(self):
            pygame.init()
            self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Исправлено: передаем кортеж
            pygame.display.set_caption("lol")
            self.clock = pygame.time.Clock()
            self.running = True
            self.first_lock = True
            self.enemy_lock = True
            self.x = 3
            #
            self.map = load_pygame(join('data', 'maps', 'world(2).tmx'))
            #
            self.all_sprites = AllSprites()
            self.collision_sprites = pygame.sprite.Group()
            self.bullet_sprites = pygame.sprite.Group()
            self.enemy_sprites = pygame.sprite.Group()

            self.can_shoot = True
            self.shoot_time = 0
            self.gun_cooldown = 300
            # audio
            self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
            self.shoot_sound.set_volume(0.3)
            self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
            self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
            self.music.set_volume(0)
            self.music.play(loops=-1)

            self.enemy_event = pygame.event.custom_type()
            pygame.time.set_timer(self.enemy_event, 1000)
            self.spawn_positions = []
            self.dungeon_positions = []

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
                pos = self.gun.rect.center + self.gun.player_direction * 50
                Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
                self.can_shoot = False
                self.shoot_time = pygame.time.get_ticks()

        def gun_timer(self):
            if not self.can_shoot:
                current_time = pygame.time.get_ticks()
                if current_time - self.shoot_time >= self.gun_cooldown:
                    self.can_shoot = True

        def setup(self):

            for x, y, image in self.map.get_layer_by_name("1").tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
            for x, y, image in self.map.get_layer_by_name("2").tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
                CollisionSprite((x, y), pygame.Surface((32, 32)),
                                self.all_sprites)
            for x, y, image in self.map.get_layer_by_name("3").tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

            for obj in self.map.get_layer_by_name('object 1'):
                CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

            for obj in self.map.get_layer_by_name("object 2"):
                if obj.name == "Player":
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                    self.gun = Gun(self.player, self.all_sprites)

                elif obj.name == "Enemy":
                    self.spawn_positions.append((obj.x, obj.y))
                    self.enemy_lock = False
                elif obj.name == "dungeon":
                    self.dungeon_positions.append((int(obj.x), int(obj.y)))

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
            collision_sprites = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False,
                                                            pygame.sprite.collide_mask)

            if collision_sprites:
                for sprite in collision_sprites:
                    sprite.destroy()
                    self.x -= 1
            if self.x == 0:
                self.running = False



        def health(self, dt):
            dest = 50
            for _ in range(self.x):
                for i in range(4):
                    im = pygame.image.load(join('images', 'Hp', 'heart.png'))
                    self.display_surface.blit(im, (dest, 30))
                dest += 40

        def run(self):
            while self.running:
                dt = self.clock.tick(60) / 1000  # Ограничиваем FPS и передаем dt в секундах

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        def is_point_in_rectangle(rect_x, rect_y, rect_width, rect_height, point_x, point_y):
                            if (rect_x <= point_x <= rect_x + rect_width) and (
                                    rect_y <= point_y <= rect_y + rect_height):
                                return True  # Точка внутри прямоугольника
                            else:
                                return False  # Точка вне прямоугольника
                        a = list(Player.coord(self.player))
                        b = list(self.dungeon_positions[0])
                        print(a)
                        print(b)
                        if is_point_in_rectangle(a[0], a[1], a[2], a[3], b[0], b[1]):
                            print('hhtf')
                            self.map = load_pygame(join('data', 'maps', 'dungeon.tmx'))
                            self.display_surface.fill('black')
                            pygame.display.flip()
                            self.setup()
                    if event.type == self.enemy_event and not self.enemy_lock:
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
                self.health(dt)
                pygame.display.flip()  # Используем flip для обновления экрана
            pygame.quit()

    game = Game()
    game.run()

