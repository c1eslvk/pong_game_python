"""
This program is a game called pong game

You can choose game mode by pressing 1 for singleplayer
and 2 for multiplayer

You can leave by pressing Esc

In singleplayer mode you use Up and Down keys to move the paddle
In multiplayer mode Player 1 uses W and S keys to move the paddle
and Player 2 uses Up and Down keys
"""
import pygame
import sys
pygame.init()
pygame.font.init()

# Creating screen
WIN_HEIGHT = 300
WIN_WIDTH = 400
scr = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
win = scr.get_rect()
pygame.display.set_caption('Pong Game')
fps = pygame.time.Clock()

# Player size
PLAYER_HEIGHT = 40
PLAYER_WIDTH = 15

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Fonts
font_end = pygame.font.SysFont('freesansbold.ttf', 30)
font_score = pygame.font.SysFont('freesansbold.ttf', 20)

# Animation
pygame.key.set_repeat(15, 15)

# Movement
k_up1 = pygame.K_w
k_down1 = pygame.K_s
k_up2 = pygame.K_UP
k_down2 = pygame.K_DOWN
k_start = pygame.K_SPACE
k_quit = pygame.K_ESCAPE
step_player = 4
vec_ball = [-1, 1]


def main_menu(win_color, screen, obj_color, obj1, obj2, obj3, obj4):
    """
    Main Menu:

    This function shows the starting screen after choosing game mode
    and allows player to start by pressing Space or exit by pressing Esc

    Function takes color of window, , color of objects and four objects
    """
    # Text
    start_text1 = font_end.render("Press Space", True, white)
    start_text2 = font_end.render("to start", True, white)
    quit_text1 = font_end.render("Press Esc", True, white)
    quit_text2 = font_end.render("to quit", True, white)

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == k_start:
                    return
                if event.key == k_quit:
                    sys.exit()

        scr.fill(win_color)
        print_object(screen, obj_color, obj1)
        print_object(screen, obj_color, obj2)
        print_object(screen, obj_color, obj3)
        print_object(screen, obj_color, obj4)
        scr.blit(start_text1, (30, 20))
        scr.blit(start_text2, (53, 40))
        scr.blit(quit_text1, (250, 20))
        scr.blit(quit_text2, (267, 40))
        pygame.display.flip()
        fps.tick(15)


def print_object(screen, color, obj):
    """
    Print Object:

    This function draws and object

    It takes screen on which object will be drawn,
    color of object and object to be drawn
    """
    pygame.draw.rect(screen, color, obj)


def write_score(font, color, value, x, y):
    """
    Write Score:

    This function show score in top right corner

    It takes font, text color, value of score and position of text
    """
    score = font.render("Score: " + str(value), True, color)
    scr.blit(score, (x, y))


def ball_movement_single(ball, box, vec_ball):
    """
    Ball Movement Single:

    This function causes object to move in singleplayer mode
    and applying collisions with window borders and one object

    It takes the object that will be moving,
    an object that the moving object will collide with
    and the vector that the object will be moving by

    It returns True if the object hits the right wall
    which allows to count points, or False if it doeasn't hit right wall
    """
    if ball.right > win.right:
        vec_ball[0] = -vec_ball[0]
        return True
    if ball.top < win.top or ball.bottom > win.bottom:
        vec_ball[1] = -vec_ball[1]
    if ball.colliderect(box):
        vec_ball[0] = -vec_ball[0]

    return False


def ball_movement_multi(ball, box1, box2, vec_ball):
    """
    Ball Movement Multi:

    This function causes object to move in multiplayer mode
    and applying collisions with top window borders and two objects

    It takes the object that will be moving,
    two objects that the moving object will collide with
    and the vector that the object will be moving by
    """
    if ball.top < win.top or ball.bottom > win.bottom:
        vec_ball[1] = -vec_ball[1]
    if ball.colliderect(box1):
        vec_ball[0] = -vec_ball[0]
    if ball.colliderect(box2):
        vec_ball[0] = -vec_ball[0]


def game_over_single(ball, value, color, font):
    """
    Game Over Single:

    This function shows the screen after losing singleplayer game
    It shows "GAME OVER" text and final score

    It takes the moving object that will tell program when player loses,
    value of score, text color and font
    """
    if ball.left < win.left:
        scr.fill((0, 0, 0))
        end_msg = font.render("GAME OVER", True, color)
        end_score = font.render(("Your score: " + str(value)), True, color)
        scr.blit(end_msg, (135, 80))
        scr.blit(end_score, (135, 150))


def game_over_multi(ball, color, font):
    """
    Game Over Multi:

    This function shows the screen after losing multiplayer game
    It shows which player won

    It takes the moving object that will tell program when player loses,
    text color and font
    """
    if ball.left < win.left:
        scr.fill((0, 0, 0))
        p1_win_msg = font.render("Player 2 wins!", True, color)
        scr.blit(p1_win_msg, (135, 80))
    if ball.right > win.right:
        scr.fill((0, 0, 0))
        p2_win_msg = font.render("Player 1 wins!", True, color)
        scr.blit(p2_win_msg, (135, 80))


def player_control(box, event, key_up, key_down):
    """
    Player Control:

    This function defines how the object will move
    and what keys will be used to control object

    It takes the object which will be controlled, event,
    and two keys which will be used to control the object

    It returns the object
    """
    if event.type == pygame.KEYDOWN:
        if event.key == key_up:
            box = box.move(0, -step_player)
        if box.y < 0:
            box.y = 0

        if event.key == key_down:
            box = box.move(0, step_player)
        if box.y > (WIN_HEIGHT - PLAYER_HEIGHT):
            box.y = (WIN_HEIGHT - PLAYER_HEIGHT)

    return box


def multiplayer():
    """
    Multiplayer:

    This is main function for multiplayer mode
    It allows you to start the game by pressing Space key
    or to leave the game by pressing Esc key
    """

    # Objects
    player1 = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball = pygame.Rect(0, 0, 10, 10)
    net = pygame.Rect(0, 0, 4, WIN_HEIGHT)
    ball.center = win.center
    player1.center = win.midleft
    player2.center = win.midright
    net.center = win.center

    main_menu(black, scr, white, player1, player2, ball, net)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            player1 = player_control(player1, event, k_up1, k_down1)
            player2 = player_control(player2, event, k_up2, k_down2)

        ball = ball.move(vec_ball)
        ball_movement_multi(ball, player1, player2, vec_ball)

        scr.fill(black)
        print_object(scr, white, player1)
        print_object(scr, white, player2)
        print_object(scr, white, ball)
        print_object(scr, white, net)
        game_over_multi(ball, white, font_end)
        pygame.display.flip()
        fps.tick(260)


def singleplayer():
    """
    Singleplayer:

    This is main function for singleiplayer mode
    It allows you to start the game by pressing Space key
    or to leave the game by pressing Esc key
    """

    # Score
    score_value = 0
    textX = 10
    textY = 10

    # Objects
    player1 = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    blank = pygame.Rect(0, 0, 0, 0)
    ball = pygame.Rect(0, 0, 10, 10)
    net = pygame.Rect(0, 0, 4, WIN_HEIGHT)
    ball.center = win.center
    player1.center = win.midleft
    blank.center = win.midright
    net.center = win.center

    main_menu(black, scr, white, player1, blank, ball, net)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            player1 = player_control(player1, event, k_up2, k_down2)

        ball = ball.move(vec_ball)
        if (ball_movement_single(ball, player1, vec_ball)):
            score_value += 1

        scr.fill(black)
        print_object(scr, white, player1)
        print_object(scr, white, ball)
        print_object(scr, white, net)
        write_score(font_score, white, score_value, textX, textY)
        game_over_single(ball, score_value, white, font_end)
        pygame.display.flip()
        fps.tick(260)


def main():
    """
    Main:

    It is main function which allows program to work properly

    It allows you to choose between Singleplayer and Mulitplayer mode
    by pressing 1 or 2 or exit using Esc
    """

    # Movement
    k_single = pygame.K_1
    k_multi = pygame.K_2

    # Text
    single_text = font_end.render("1. Singleplayer", True, white)
    multi_text = font_end.render("2. Multiplater", True, white)
    welcome_text = font_end.render("Welcome to pong game!", True, white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == k_single:
                    singleplayer()
                if event.key == k_multi:
                    multiplayer()
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        scr.fill(black)
        scr.blit(welcome_text, (70, 50))
        scr.blit(single_text, (120, 120))
        scr.blit(multi_text, (120, 170))
        pygame.display.flip()


if __name__ == '__main__':
    main()
