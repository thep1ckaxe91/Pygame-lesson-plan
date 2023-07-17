from random import randint
import pygame,math,sys,time,os
from pygame.math import Vector2
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 1366,768
WHITE = (255,255,255)
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont("arial",200)
GUIDE_FONT = pygame.font.SysFont("arial",50)
SCORE_FONT = pygame.font.SysFont("calibri",50)
player_1_score_text = SCORE_FONT.render("0",True,WHITE)
player_2_score_text = SCORE_FONT.render("0",True,WHITE)
# match end after player reach 10 score
# a round end when ball pass any player
path = os.path.dirname(os.path.abspath(__file__))
won_sfx = pygame.mixer.Sound(path+"/assets/won.wav")
ball_hit_sfx = pygame.mixer.Sound(path+"/assets/ball_hit.wav")

game_active = False
in_main_menu = True
in_game_over = False

player_width = 20
player_height = 150
player_offset_x = 20
player_speed = 10
player_1_turn = True
player_1_score = 0
player_2_score = 0
player_1_rect = pygame.Rect(
    player_offset_x,
    HEIGHT/2-player_height/2,
    player_width,
    player_height
)
player_2_rect = pygame.Rect(
    WIDTH-player_width-player_offset_x,
    HEIGHT/2-player_height/2,
    player_width,
    player_height
)
ball_edge_size = 20
ball_init_vel = 7
ball_vel = Vector2(ball_init_vel,0)

ball_rect = pygame.Rect(
    WIDTH/2-ball_edge_size/2,
    HEIGHT/2-ball_edge_size/2,
    ball_edge_size,
    ball_edge_size
)

def init_ball():
    ball_rect.center = (WIDTH/2,HEIGHT/2)
    if player_1_turn:
        ball_vel.x = -ball_init_vel
    else:
        ball_vel.x = ball_init_vel
    ball_vel.y = 0
    ball_vel.rotate_ip(randint(-30,30))
init_ball()

def reset_round(player_won : int):
    global player_1_score,player_2_score,player_1_turn,player_1_score_text,player_2_score_text
    player_1_score += player_won == 1
    player_2_score += player_won == 2
    player_1_score_text = SCORE_FONT.render(str(player_1_score),True,WHITE)
    player_2_score_text = SCORE_FONT.render(str(player_2_score),True,WHITE)
    player_1_turn = not (player_won == 1)
    init_ball()
    won_sfx.play()

def collision_handler():
    # collide with edge screen
    global served,ball_vel
    if ball_rect.top + ball_vel.y < 0 :
        ball_vel.y = -ball_vel.y
        ball_rect.top = -ball_rect.top
        ball_hit_sfx.play()
    elif ball_rect.bottom + ball_vel.y > HEIGHT:
        ball_vel.y = -ball_vel.y
        ball_rect.bottom = 2*HEIGHT - ball_rect.bottom
        ball_hit_sfx.play()
    
    if ball_rect.colliderect(player_1_rect):
        collidex = player_1_rect.right-ball_rect.left
        ball_rect.centerx += collidex
        ball_rect.centery += collidex*ball_vel.y/ball_vel.x
        ball_vel = Vector2(ball_rect.center) - (player_1_rect.centerx - player_height/2,player_1_rect.centery)
        ball_vel.scale_to_length(ball_init_vel*2)
        ball_hit_sfx.play()
    elif ball_rect.colliderect(player_2_rect):
        collidex = player_2_rect.left-ball_rect.right
        ball_rect.centerx += collidex
        ball_rect.centery += collidex*ball_vel.y/ball_vel.x
        ball_vel = Vector2(ball_rect.center) - (player_2_rect.centerx + player_height/2,player_2_rect.centery)
        ball_vel.scale_to_length(ball_init_vel*2)
        ball_hit_sfx.play()
    

def update():
    global game_active,in_game_over
    if game_active:
        global in_game_over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_1_rect.y -= player_speed
        if keys[pygame.K_s]:
            player_1_rect.y += player_speed
        player_1_rect.clamp_ip(player_1_rect.x,0,player_width,HEIGHT)
        if keys[pygame.K_UP]:
            player_2_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_2_rect.y += player_speed
        player_2_rect.clamp_ip(player_2_rect.x,0,player_width,HEIGHT)
        
        ball_rect.center += ball_vel

        collision_handler()

        if ball_rect.left < -50:
            reset_round(2)
        elif ball_rect.right > WIDTH+50:
            reset_round(1)
        
        if player_1_score >= 10:
            in_game_over = True
            game_active = False
        elif player_2_score >= 10:
            in_game_over = True
            game_active = False
        

def draw_score():
    window.blit(player_1_score_text,(WIDTH/2-player_1_score_text.get_width()-10,10))
    window.blit(player_2_score_text,(WIDTH/2+10,10))

def draw_net():
    pygame.draw.line(window,WHITE,(WIDTH/2,0),(WIDTH/2,HEIGHT),2)

def draw_player():
    pygame.draw.rect(window,WHITE,player_1_rect)
    pygame.draw.rect(window,WHITE,player_2_rect)

def draw_ball():
    pygame.draw.rect(window,WHITE,ball_rect)
    
def draw_screen():
    window.fill('black')
    if game_active:
        draw_player()
        draw_ball()
        draw_score()
        draw_net()
    else:
        if in_main_menu:
            title_text = TITLE_FONT.render("PONG",True,WHITE)
            guide_text = GUIDE_FONT.render("Press SPACE to start",True,WHITE)
            window.blit(title_text,(WIDTH/2-title_text.get_width()/2,HEIGHT/2-title_text.get_height()))
            window.blit(guide_text,(WIDTH/2-guide_text.get_width()/2,HEIGHT/2+guide_text.get_height()))
        elif in_game_over:
            if player_1_turn:
                title_text = TITLE_FONT.render("Player 2 Won",True,WHITE)
            else:
                title_text = TITLE_FONT.render("Player 1 Won",True,WHITE)
            guide_text = GUIDE_FONT.render("Press SPACE to start",True,WHITE)
            window.blit(title_text,(WIDTH/2-title_text.get_width()/2,HEIGHT/2-title_text.get_height()))
            window.blit(guide_text,(WIDTH/2-guide_text.get_width()/2,HEIGHT/2+guide_text.get_height()))
    

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_active = False
                    in_main_menu = True
            if in_main_menu:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    in_main_menu = False
            elif in_game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    in_game_over = False
                    player_1_score,player_2_score = 0,0
                    init_ball()
                    player_1_rect.centery = HEIGHT/2
                    player_2_rect.centery = HEIGHT/2
                    player_1_score_text = SCORE_FONT.render("0",True,WHITE)
                    player_2_score_text = SCORE_FONT.render("0",True,WHITE)

        update()
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
        
