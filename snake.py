import pygame
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = str(540) + "," + str(150)

pygame.init()

display_width = 400
display_height = 500

black = (0, 0, 0)
dark_blue = (5, 0, 128)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (64, 64, 64)

dimension = 10

food_x = random.randint(0, 39) * dimension
food_y = random.randint(0, 39) * dimension

score = 0
speed_x = 0
speed_y = 0
length = 1

snake_x = [200]
snake_y = [200]

clock = pygame.time.Clock()
crash_sound = pygame.mixer.Sound("crash.wav")

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(f'Score :{score}', True, green, dark_blue)
textRect = text.get_rect()
textRect.center = (200, 450)


def food():
    global food_x, food_y
    pygame.draw.rect(gameDisplay, red, [food_x, food_y, dimension, dimension])


def snake():
    global snake_x, snake_y
    for j in range(score + 1):
        pygame.draw.rect(gameDisplay, white, [snake_x[j], snake_y[j], dimension, dimension])


def new_food():
    global food_y, food_x
    food_x = random.randint(0, 39) * dimension
    food_y = random.randint(0, 39) * dimension
    for k in range(score + 1):
        if food_x == snake_x[k] and food_y == snake_y[k]:
            new_food()


game_over = False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x = -dimension
                speed_y = 0
            if event.key == pygame.K_RIGHT:
                speed_x = dimension
                speed_y = 0
            if event.key == pygame.K_UP:
                speed_y = -dimension
                speed_x = 0
            if event.key == pygame.K_DOWN:
                speed_y = dimension
                speed_x = 0

    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay, grey, [0, 400, 400, 100])
    text = font.render(f'Score :{score}', True, green, dark_blue)
    gameDisplay.blit(text, textRect)

    for i in range(score):
        snake_x[score - i] = snake_x[score - i - 1]
        snake_y[score - i] = snake_y[score - i - 1]

    snake_x[0] += speed_x
    snake_y[0] += speed_y

    if (food_x == snake_x[0]) and (food_y == snake_y[0]):
        score += 1
        snake_x.insert(0, snake_x[0] + speed_x)
        snake_y.insert(0, snake_y[0] + speed_y)
        pygame.mixer.Sound.play(crash_sound)
        pygame.mixer.music.stop()
        new_food()

    if snake_x[0] < 0:
        snake_x[0] = 390
    elif snake_x[0] > 390:
        snake_x[0] = 0
    if snake_y[0] < 0:
        snake_y[0] = 390
    elif snake_y[0] > 390:
        snake_y[0] = 0

    if score >= 1:
        for i in range(1, score + 1):
            if snake_x[i] == snake_x[0] and snake_y[i] == snake_y[0]:
                game_over = True

    snake()
    food()

    clock.tick(15 + score)

    pygame.display.update()
