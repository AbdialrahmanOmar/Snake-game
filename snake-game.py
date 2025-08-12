# main.py
import pygame
import random
import sys

pygame.init()

# Settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake and food setup
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = (CELL_SIZE, 0)
food = (200, 200)
score = 0
energy = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
            elif event.key == pygame.K_p:
                paused = not paused

    if not paused:
        head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, head)
        if head == food:
            score += 1
            energy = min(100, energy + 10)
            food = (random.randrange(0, WIDTH, CELL_SIZE),
                    random.randrange(0, HEIGHT, CELL_SIZE))
        else:
            snake.pop()

        energy -= 0.5
        if energy <= 0 or head in snake[1:] or not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            running = False

    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(
            screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Score: {score}  Energy: {int(energy)}", True, WHITE)
    screen.blit(text, (5, 5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
