# snake_game.py
import pygame
import random
import sys

pygame.init()

# --- Basic Settings ---
WIDTH, HEIGHT = 600, 400       # window size
BLOCK_SIZE = 20                # size of each snake piece
SPEED = 10                     # game speed (frames per second)

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (40, 200, 40)
RED = (220, 50, 50)

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Keep track of high score (only lasts while program runs)
high_score = 0


# ---------------- Helper bits ----------------
def new_food():
    """Pick a random spot on the grid for food to appear."""
    return (random.randrange(0, WIDTH, BLOCK_SIZE),
            random.randrange(0, HEIGHT, BLOCK_SIZE))


def draw_snake(body):
    for part in body:
        pygame.draw.rect(screen, GREEN, (*part, BLOCK_SIZE, BLOCK_SIZE))


def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, BLOCK_SIZE, BLOCK_SIZE))


def draw_status(score, energy_left):
    font = pygame.font.SysFont("Arial", 22)
    hud = font.render(f"Score: {score}   Energy: {int(energy_left)}", True, WHITE)
    screen.blit(hud, (10, 10))


def show_menu():
    """Main menu before starting."""
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    option_font = pygame.font.SysFont("Arial", 26)

    title = title_font.render("SNAKE GAME", True, GREEN)
    start = option_font.render("Press SPACE to Start", True, WHITE)
    quit_msg = option_font.render("Press Q to Quit", True, WHITE)
    high_msg = option_font.render(f"High Score: {high_score}", True, RED)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
    screen.blit(quit_msg, (WIDTH//2 - quit_msg.get_width()//2, HEIGHT//1.5))
    screen.blit(high_msg, (WIDTH//2 - high_msg.get_width()//2, HEIGHT//1.2))

    pygame.display.flip()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def show_game_over(final_score):
    """Game Over screen with restart/quit options."""
    screen.fill(BLACK)
    big_font = pygame.font.SysFont("Arial", 40, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)

    over_text = big_font.render("GAME OVER!", True, RED)
    score_text = small_font.render(f"Your Score: {final_score}", True, WHITE)
    restart_text = small_font.render("Unlucky, try again! Press R", True, WHITE)
    quit_text = small_font.render("Press Q to Quit", True, WHITE)

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//1.5))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//1.3))

    pygame.display.flip()

    # Wait for R or Q
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# ---------------- Main game loop ----------------
def play():
    global high_score

    # starting snake & food
    snake = [(100, 100), (80, 100), (60, 100)]
    move_dir = (BLOCK_SIZE, 0)
    food = new_food()

    score = 0
    energy = 100
    paused = False
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and move_dir != (0, BLOCK_SIZE):
                    move_dir = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and move_dir != (0, -BLOCK_SIZE):
                    move_dir = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and move_dir != (BLOCK_SIZE, 0):
                    move_dir = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and move_dir != (-BLOCK_SIZE, 0):
                    move_dir = (BLOCK_SIZE, 0)
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            # move the snake forward
            head_x, head_y = snake[0]
            new_head = (head_x + move_dir[0], head_y + move_dir[1])
            snake.insert(0, new_head)

            # if food eaten
            if new_head == food:
                score += 1
                energy = min(100, energy + 12)
                food = new_food()
            else:
                snake.pop()  # chop tail if no food

            # snake loses energy every move
            energy -= 0.4

            # check death conditions
            hit_wall = not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT)
            hit_self = new_head in snake[1:]

            if energy <= 0 or hit_wall or hit_self:
                if score > high_score:
                    high_score = score
                restart = show_game_over(score)
                return restart

        # Drawing stuff
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_status(score, energy)

        pygame.display.flip()
        clock.tick(SPEED)


# ---------------- Main Program Loop ----------------
while True:
    show_menu()
    if not play():
        break
