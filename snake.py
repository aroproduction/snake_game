import pygame
import random
import sys

pygame.init()

# Define colors
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Aritra')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 8.5

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

score = 0

boundary_color = (255, 255, 255)  # white


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, red)
    dis.blit(value, [dis_width - 200, 10])


def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def generate_food(snake_list):
    margin = 50  # Margin from the border
    while True:
        foodx = round(random.randrange(margin, dis_width - snake_block - margin) / 20.0) * 20.0
        foody = round(random.randrange(margin, dis_height - snake_block - margin - 50) / 20.0) * 20.0  # Subtract 50 to avoid "Your Score" text region
        if [foodx, foody] not in snake_list:  # Check if the food is not in the snake's body
            return foodx, foody

def pause_game():
    paused = True
    message("Paused", blue, y_displace=-50)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press P again to unpause
                    paused = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(5)


def game_intro():
    intro = True

    while intro:
        dis.fill(black)
        message("Welcome to Snake Game", green, -50)
        message("Press P to Play or Q to Quit", blue, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    intro = False

    gameLoop()


def gameLoop():
    global score, x1, y1
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx, foody = generate_food(snake_list)

    game_over = False
    game_close = False

    while not game_over:

        while game_close == True:
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red, -50)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_f:  # Press F for Full Screen
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_p:  # Press P to pause
                    pause_game()
                elif event.key == pygame.K_q:
                    game_close = True

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, boundary_color, [0, 0, dis_width, dis_height], 5)

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_list)
            length_of_snake += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_intro()
