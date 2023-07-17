from random import randint
import pygame,math,sys,time,os
from pygame import Vector2
pygame.init()
scale = 2
gravity = 0.2*scale
tile_size = 32*scale
WIDTH,HEIGHT = tile_size*9,tile_size*16
ground_height = tile_size*3
bird_size = tile_size*2

window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

path = os.path.dirname(os.path.abspath(__file__))
background_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/background_day.png'),(WIDTH,HEIGHT))
ground_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/ground.png'),(WIDTH,ground_height))


bird_sprites = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/bird.png'),(bird_size*4,bird_size))
bird_img_id = 0
bird_anim_delay = 5
bird_anim_cnt = 0
bird_pos = Vector2(WIDTH/2 - bird_size/2,HEIGHT/2 - bird_size/2)
bird_vely = 0.0
bird_jump_vel = 10
bird_img = pygame.Surface((bird_size,bird_size),pygame.SRCALPHA)

def draw_screen():
    window.fill("black")
    window.blit(background_img,(0,0))
    window.blit(ground_img,(0,HEIGHT-ground_height))
    window.blit(bird_img,bird_pos)

def update_bird():
    global bird_img_id,bird_anim_cnt,bird_vely
    bird_anim_cnt+=1
    if bird_anim_cnt >= bird_anim_delay:
        bird_img_id+=1
        bird_img_id%=4
        bird_anim_cnt -= bird_anim_delay
    bird_img.blit(bird_sprites,(0,0),(bird_img_id*bird_size,0,bird_size,bird_size))
    bird_vely += gravity
    bird_pos.y += bird_vely
    

def update():
    update_bird()


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bird_pos.xy = (WIDTH/2-bird_size/2,HEIGHT/2-bird_size/2)
                    bird_vely = 0
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird_vely = -bird_jump_vel
        update()
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
