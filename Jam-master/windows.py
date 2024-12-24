import pygame
import sys
import pygame.mixer
import sqlite3
import random
import cv2
import main



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
            self.image_ch0 = pygame.image.load(image_ch)
            self.image_ch0 = pygame.transform.scale(self.image_ch0, (width, height))
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

video_path = 'video/1run.mp4'
cap = cv2.VideoCapture(video_path)

clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
bg = pygame.image.load("menu_assets/N.png")
bg1 = pygame.image.load("menu_assets/Start.jpg")
bg2 = pygame.image.load("menu_assets/zaq.jpg")
bg3 = pygame.image.load("menu_assets/q.jpg")
bg4 = pygame.image.load("menu_assets/Gear.jpeg")
image4 = pygame.transform.scale(bg4, (800, 600))
image12 = pygame.transform.scale(bg2, (800, 600))
image = pygame.transform.scale(bg1, (800, 600))
image123 = pygame.transform.scale(bg3, (800, 600))
screen = pygame.display.set_mode(size)
pygame.mixer.music.load('music/Menu_tr.mp3')
pygame.mixer.music.play(-1)


def menu():
    screen = pygame.display.set_mode(size)
    st_but = Button(width / 2 - (252 / 2), 150, 252, 74, 'Новая игра', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sett_but = Button(width / 2 - (252 / 2), 250, 252, 74, 'Настройки', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    exit_but = Button(width / 2 - (252 / 2), 350, 252, 74, 'Выйти', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [st_but, sett_but, exit_but]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT and event.button == sett_but:
                sett()
            if event.type == pygame.USEREVENT and event.button == exit_but:
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == st_but:
                lev()
            for i in sp:
                i.hand_ev(event)
        ret, frame = cap.read()

        # Если достигнут конец видео, перезапускаем его
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Перейти к первому фрейму
            continue

        # Преобразуем BGR в RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Преобразуем в формат Pygame
        frame = pygame.surfarray.make_surface(frame)
        width_new, height_new = 800, 600
        frame = pygame.transform.scale(frame, (width_new, height_new))


        # Отображаем фрейм
        screen.blit(frame, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Hangover 4', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()

        clock.tick(20)

    pygame.quit()


def sett():
    exit_but = Button(width / 2 - (252 / 2), 450, 252, 74, 'Назад', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    reg_but = Button(width / 2 - (252 / 2), 350, 240, 74, 'Регистрация', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [exit_but, reg_but]
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 32)

    def nothing():
        pass

    class InputBox:

        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_ACTIVE
            self.text = text
            self.txt_surface = FONT.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = COLOR_INACTIVE if self.active else COLOR_ACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print('АХАХАХАХАХАХАХАХА')
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

                    self.txt_surface = FONT.render(self.text, True, self.color)


        def regist(self):
            return self.text
            self.text = ''

        def update(self):
            width = max(200, self.txt_surface.get_width() + 10)
            self.rect.w = width

        def draw(self, screen):
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)

    input_box1 = InputBox(300, 200, 140, 32)
    input_box2 = InputBox(300, 270, 140, 32)
    input_boxes = [input_box1, input_box2]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.USEREVENT and event.button == exit_but:
                menu()
            if event.type == pygame.USEREVENT and event.button == reg_but:
                a = input_box1.regist()
                b = input_box2.regist()
                con = sqlite3.connect('tab.db')
                cur = con.cursor()
                result = cur.execute("""SELECT name from users""").fetchall()
                sp = [el[0] for el in result]
                if a not in sp:
                    cur.execute(f"INSERT INTO users VALUES ('{a}', '{b}')")
                    con.commit()
                    window(1)
                    con.close()
                else:
                    window(0)



            for i in sp:
                i.hand_ev(event)
        screen.fill((0, 0, 0))
        screen.blit(bg, (-40, -200))
        for box in input_boxes:
            box.update()
        for box in input_boxes:
            box.draw(screen)
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Settings', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


def lev():
    l_1 = Button(100, 150, 150, 131, '1', 'menu_assets/lev1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    l_2 = Button(350, 150, 150, 131, '2', 'menu_assets/lev1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    l_3 = Button(600, 150,150, 131, '3', 'menu_assets/lev1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    exit_but = Button(width / 2 - (252 / 2), 350, 252, 74, 'Назад', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [l_1, l_2, l_3, exit_but]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False
            if event.type == pygame.USEREVENT and event.button == exit_but:
                menu()
            if event.type == pygame.USEREVENT and event.button == l_1:
                main.play()
            if event.type == pygame.USEREVENT and event.button == l_2:
                main.play()
            if event.type == pygame.USEREVENT and event.button == l_3:
                main.play()
            for i in sp:
                i.hand_ev(event)
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Levels', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

def win(f):
    size = width, height = (800, 600)
    exit_but = Button(width / 2 - (252 / 2), 450, 252, 74, 'Заново', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [exit_but]
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('music/win_m.mp3')
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == exit_but:
                pygame.mixer.music.load('music/Menu_tr.mp3')
                pygame.mixer.music.play(-1)
                if f == 1:
                    main.play()
                elif f == 2:
                    main.play()
                elif f == 3:
                    main.play()
            for i in sp:
                i.hand_ev(event)
        screen.fill((0, 0, 0))
        screen.blit(image12, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Вы победили', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(10)
    pygame.quit()


def lose(f):
    size = width, height = (800, 600)
    exit_but = Button(width / 2 - (252 / 2), 450, 252, 74, 'Заново', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [exit_but]
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('music/lose.mp3')
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT and event.button == exit_but:
                pygame.mixer.music.load('music/Menu_tr.mp3')
                pygame.mixer.music.play(-1)
                if f == 1:
                    main.play()
                elif f == 2:
                    main.play()
                elif f == 3:
                    main.play()

            for i in sp:
                i.hand_ev(event)
        screen.fill((0, 0, 0))
        screen.blit(image123, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('Потрачено', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


def window(f):
    pygame.init()
    size = width, height = (800, 600)
    exit_but = Button(width / 2 - (252 / 2), 450, 252, 74, 'Назад', 'menu_assets/1.png', 'music/kn2.mp3', 'menu_assets/chang.png')
    sp = [exit_but]
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('music/the witcher.mp3')
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT and event.button == exit_but:
                pygame.mixer.music.load('music/Menu_tr.mp3')
                pygame.mixer.music.play(-1)
                sett()
            for i in sp:
                i.hand_ev(event)
        screen.fill((0, 0, 0))
        screen.blit(image4, (0, 0))
        font = pygame.font.Font(None, 50)
        if f == 1:
            text_surface = font.render('Вы зарегистрировались или вошли', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, 100))
            screen.blit(text_surface, text_rect)
        else:
            text_surface = font.render('Вы  не зарегистрировались', True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width / 2, 100))
            screen.blit(text_surface, text_rect)
        for j in sp:
            j.draw(screen)
            j.check(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()



menu()