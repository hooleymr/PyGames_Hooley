from tkinter import font
import pygame, sys
import random
import os

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time #USE A CLASS
    #MOVE BALL
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #Collisions
    if ball.top <= 0 or ball.bottom >= screen_height: #TOP BOTTOM DETECT IF GOES BEYOND SCREEN BOUNDS
        ball_speed_y *= -1 #REVERSE BALL SPEED
        pygame.mixer.Sound.play(pong_sound)

    if ball.left <= 0:  
        pygame.mixer.Sound.play(score_sound)
        player_score+=1
        score_time = pygame.time.get_ticks() #how long has it been since game started

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score+=1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0: #checks collision and current ball direction
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10 : #check if ball collides with top/bottom of paddle
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *=-1 
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *=-1 

    if ball.colliderect(opponent) and ball_speed_x < 0: #checks collision and current ball direction
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10 :
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *=-1
        elif abs(ball.bottom - opponent.bottom) < 10 and ball_speed_y > 0:
            ball_speed_y *=-1 

def player_animation():
    player.y += player_speed

    #PLAYER BOUNDARY COLLISIONS
    if player.top <= 0 :
        player.top = 0
    if player.bottom >= screen_height: #screen goes top to bottom, 0 at top, screen_height at bottom
        player.bottom = screen_height 

def opponent_ai():
    if opponent.top <= 0 :
        opponent.top = 0
    if opponent.bottom >= screen_height: #screen goes top to bottom, 0 at top, screen_height at bottom
        opponent.bottom = screen_height 

    if opponent.top < ball.y: #ball.center is a tuple, need an int
        opponent.top += opponent_speed #+ to go down since screen is built top to bottom
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time #USE A CLASS

    current_time = pygame.time.get_ticks() #called repeatedly
    ball.center = (screen_width/2, screen_height/2)

    if(current_time - score_time < 700):
        num_three = game_font.render("3", False, light_grey)
        screen.blit(num_three, (screen_width/2 - 10, screen_height/2 + 20))
    if(700 < current_time - score_time < 1400):
        num_two = game_font.render("2", False, light_grey)
        screen.blit(num_two, (screen_width/2 - 10, screen_height/2 + 20))
    if(1400 < current_time - score_time < 2100):
        num_one = game_font.render("1", False, light_grey)
        screen.blit(num_one, (screen_width/2 - 10, screen_height/2 + 20))

    if(current_time - score_time < 2100):
        ball_speed_x, ball_speed_y = 0,0
    else: #RANDOMIZE DIRECTION ON RESET
        ball_speed_y = 7 * random.choice((1,-1))
        ball_speed_x = 7 * random.choice((1,-1))
        score_time = None


#SOUND INIT AND SETUP
pygame.mixer.pre_init(44100, -16, 2, 512) #adjust sound buffer size during pre init
pygame.init()
timer = pygame.time.Clock()

#WINDOW
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#RECTANGLES
ball_height = 30
ball_width = 30
ball = pygame.Rect(screen_width/2 - (ball_width/2), screen_height/2-(ball_height/2), ball_width, ball_height) #pixels high, pixels wide, BASED ON TOP LEFT OF SHAPE

player = pygame.Rect(screen_width-20, screen_height/2-70, 10, 140)
opponent = pygame.Rect(10, screen_height/2-70, 10, 140)

#COLORS RGB
bg_color = (47,79,79) 
light_grey = (197,193,170)

#GAME VARIABLES
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

#TEXT
player_score = 0
opponent_score = 0
font_size = 35

game_font = pygame.font.Font("freesansbold.ttf", font_size) #font, fontsize


#SCORE TIMER
score_time = True

#SOUNDS
pong_sound = pygame.mixer.Sound("pong.wav")
score_sound = pygame.mixer.Sound("score.wav")

#LOOP
while True:
    #input handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #check if user quits
            pygame.quit() #unitialize pygame
            sys.exit() #exit the window

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN: #K_DOWN is down arrow
                player_speed += 7
            if event.key == pygame.K_UP: #UP BUTTON
                player_speed -=7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN: #K_DOWN is down arrow
                player_speed -= 7
            if event.key == pygame.K_UP: #UP BUTTON
                player_speed +=7

    #visuals DRAWN IN ORDERED LAYERS BOTTOM TO TOP
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,0), (screen_width/2, screen_height))

    player_text = game_font.render(f"{player_score}", False, light_grey) #font, AA T/F, color
    screen.blit(player_text, (screen_width/2+(font_size//2), screen_height/2-font_size)) #attatch text surface to game surface, position MUST BE ON TOP OF GAME SURFACE

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey) #font, AA T/F, color
    screen.blit(opponent_text, (screen_width/2-(font_size),screen_height/2-font_size)) #attatch text surface to game surface, position MUST BE ON TOP OF GAME SURFACE

    ball_animation()
    player_animation()
    opponent_ai()

    if score_time:
        ball_restart()


    #update window
    pygame.display.flip()
    timer.tick(60) #number of flips per second, CPU tries to run as fast as possible, too fast is possible

#DISPLAY SURFACE (unique)-> REGULAR SURFACE (essentially div) -> RECT(just a rectangle, can put it around shapes and divs to measure etc...)

#BASIC OPPONENT AI: 
#OPPONENT TOP > BALL CENTER : MOVE DOWN
#OPPONENT BOTTOM < BALL CENTER : MOVE UP
#SPEED OF OPPONENT = DIFFICULTY