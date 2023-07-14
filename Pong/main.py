from random import randint
import pygame,math,sys,time
from pygame.math import Vector2
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 1366,768
WHITE = (255,255,255)
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont("Calibri",50)

# match end after player reach 10 score
# a round end when ball pass any player
won_sfx = pygame.mixer.Sound("assets/won.wav")
ball_hit_sfx = pygame.mixer.Sound("assets/ball_hit.wav")

game_active = True

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
    global player_1_score,player_2_score,player_1_turn
    player_1_score += player_won == 1
    player_2_score += player_won == 2
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
    

def fixedUpdate():
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

def draw_score():
    player_1_score_text = SCORE_FONT.render(str(player_1_score),True,WHITE)
    player_2_score_text = SCORE_FONT.render(str(player_2_score),True,WHITE)
    window.blit(player_1_score_text,(WIDTH/2-player_1_score_text.get_width()-10,10))
    window.blit(player_2_score_text,(WIDTH/2+10,10))

def draw_net():
    pygame.draw.line(window,WHITE,(WIDTH/2,0),(WIDTH/2,HEIGHT),2)

def draw_player():
    pygame.draw.rect(window,WHITE,player_1_rect)
    pygame.draw.rect(window,WHITE,player_2_rect)

def draw_ball():
    pygame.draw.rect(window,WHITE,ball_rect)

def drawScreen():
    window.fill('black')
    if game_active:
        draw_player()
        draw_ball()
        draw_score()
        draw_net()
    else:
        
    

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fixedUpdate()
        drawScreen()
        pygame.display.flip()
        clock.tick(60)
        
