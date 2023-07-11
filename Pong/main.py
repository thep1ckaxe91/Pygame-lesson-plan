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
ball_rect = pygame.Rect()


def fixedUpdate():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_1_rect.y -= player_speed
    if keys[pygame.K_s]:
        player_1_rect.y += player_speed
    if keys[pygame.K_UP]:
        player_2_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_2_rect.y += player_speed

def drawScreen():
    window.fill('black')
    pygame.draw.rect(window,WHITE,player_1_rect)
    pygame.draw.rect(window,WHITE,player_2_rect)


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
        
