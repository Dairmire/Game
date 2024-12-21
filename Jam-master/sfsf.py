import cv2
import pygame

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# Загружаем видеофайл
video_path = '1run.mp4'
cap = cv2.VideoCapture(video_path)

# Цикл для отображения видео
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Читаем фрейм из видео
    ret, frame = cap.read()

    # Если достигнут конец видео, перезапускаем его
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Перейти к первому фрейму
        continue

    # Преобразуем BGR в RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Преобразуем в формат Pygame
    frame = pygame.surfarray.make_surface(frame)

    # Отображаем фрейм
    screen.blit(frame, (0, 0))
    pygame.display.flip()
    clock.tick(30)

# Освобождаем ресурсы
cap.release()
pygame.quit()
