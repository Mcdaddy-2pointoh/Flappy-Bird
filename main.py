import pygame as pg
import sys
import random

pg.init()

# Creates Canvas for display
screen = pg.display.set_mode((288, 512))

# Clock and screen rate management
clock = pg.time.Clock()

# Font
game_font = pg.font.Font("./Font/04B_19.TTF", 40)
game_font_small = pg.font.Font("./Font/04B_19.TTF", 25)


def score_disp(game_state):

    if game_state == 'game_on':
        score_surface = game_font.render("Score " + str(int(score)), True, (255, 255, 255))
        score_obj = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_obj)

    elif game_state == 'game_over':
        score_surface = game_font.render("Score " + str(int(score)), True, (255, 255, 255))
        score_obj = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_obj)

        high_score_surface = game_font.render("High Score " + str(int(high_score)), True, (255, 255, 255))
        high_score_obj = high_score_surface.get_rect(center=(144, 90))
        screen.blit(high_score_surface, high_score_obj)



# Background Image
bg = pg.image.load("./Images/bg.png").convert()

# Base
base = pg.image.load("./Images/base.png").convert()
base_x_position = 0


def base_disp():
    screen.blit(base, (base_x_position + 288, 450))
    screen.blit(base, (base_x_position, 450))


# Bird
bird_mid = pg.image.load("./Images/bird2.png").convert_alpha()
bird_up = pg.image.load("./Images/bird3.png").convert_alpha()
bird_down = pg.image.load("./Images/bird1.png").convert_alpha()
bird_cycle = [bird_down, bird_mid, bird_up, bird_mid]
bird_index = 0
bird_center = bird_cycle[bird_index]
bird_obj = bird_center.get_rect(center=(48, 256))
BIRDFLAP = pg.USEREVENT + 1
pg.time.set_timer(BIRDFLAP, 200)


def bird_disp(bird):
    screen.blit(bird, bird_obj)


def rotate_bird(bird):
    new_bird = pg.transform.rotozoom(bird, -bird_movement * 5, 1)
    return new_bird


def animate_bird():
    new_bird = bird_cycle[bird_index]
    new_bird_rect = new_bird.get_rect(center=(48, bird_obj.centery))
    return new_bird, new_bird_rect


# Pipe
pipe = pg.image.load("./Images/pipe.png")
SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, 1000)
pipe_list = []


def create_pipe():
    height_floor = random.randint(80, 250)
    void = random.randint(100, 150)
    height_base = height_floor + void
    top_pipe = pipe.get_rect(midbottom=(300, height_floor))
    bottom_pipe = pipe.get_rect(midtop=(300, height_base))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 1.50
    return pipes


def pipe_disp(pipes):
    for p in pipes:
        if p.top <= 0:
            flip_pipe = pg.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, p)

        else:
            screen.blit(pipe, p)


# Game Physics
gravity = 0.16
bird_movement = 0
game_active = True
score = 0
high_score = 0


def collision(pipes):
    for p in pipes:
        if bird_obj.colliderect(p):
            return False

    if bird_obj.top <= 0:
        return False

    elif bird_obj.bottom >= 450:
        return False

    else:
        return True


while True:
    # Input and pre-defined events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        # Key Record
        if event.type == pg.KEYDOWN:
            # To Jump
            if event.key == pg.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5

            # To start game
            elif event.key == pg.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_obj = bird_center.get_rect(center=(48, 256))
                bird_movement = 0

        # To generate pipe SPAWN
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        # To animate Bird flap
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1

            else:
                bird_index = 0

            bird_center, bird_obj = animate_bird()

    # Function to check collision
    game_active = collision(pipe_list)

    # Displays background on the screen
    screen.blit(bg, (0, 0))

    if game_active:
        # Display pipes on the screen
        pipe_list = move_pipes(pipe_list)
        pipe_disp(pipe_list)

        # Displays bird on the screen with physics
        bird_movement += gravity
        bird_obj.centery += bird_movement
        rotated_bird = rotate_bird(bird_center)
        bird_disp(rotated_bird)

        # Displays score on the screen
        score += 0.0075
        score_disp('game_on')

    else:
        score_disp('game_over')

    # Displays base on the screen
    if base_x_position < - 288:
        base_x_position = 0
    base_x_position -= 1
    base_disp()

    # Update adds any image/object on the predefined canvas
    pg.display.update()

    # Frame Limiter
    clock.tick(120)
