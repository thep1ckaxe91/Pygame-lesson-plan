from random import randint
import pygame,math,sys,time
pygame.init()
WIDTH,HEIGHT = 1366,768
refresh_rate = 60
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
player_width = 20
player_height = 150
player_offset_x = 20
player_speed = 5
player_1_turn = True
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
ball_init_vel = 5
ball_vel = pygame.math.Vector2(ball_init_vel,0)

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

def collision_handler():
    if ball_rect.top + ball_vel.y < 0 :
        ball_rect.x += ball_vel.x
        ball_rect.y += ball_rect.y-
        ball_vel.y = -ball_vel.y
    if ba

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


def draw_player():
    pygame.draw.rect(window,WHITE,player_1_rect)
    pygame.draw.rect(window,WHITE,player_2_rect)

def draw_ball():
    pygame.draw.rect(window,WHITE,ball_rect)

def drawScreen():
    window.fill('black')
    draw_player()
    draw_ball()


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
        
