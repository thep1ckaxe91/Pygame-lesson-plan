from random import randint, randrange
import pygame,math,sys,time,os
from pygame import Vector2
pygame.init()
scale = 2
gravity = 0.3*scale
tile_size = 32*scale
WIDTH,HEIGHT = tile_size*9,tile_size*16
ground_height = tile_size*3
bird_size = tile_size*2
relative_scale = bird_size//32

window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

path = os.path.dirname(os.path.abspath(__file__))
background_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/background_day.png'),(WIDTH,HEIGHT))
ground_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/ground.png'),(WIDTH,ground_height))


bird_sprites = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/bird.png'),(bird_size*4,bird_size))
bird_img_id = 0
bird_anim_delay = 5
bird_anim_cnt = 0
bird_pos = Vector2(WIDTH/3 - bird_size/2,HEIGHT/2 - bird_size/2)
bird_vely = 0.0
bird_jump_vel = 12
bird_img = pygame.Surface((bird_size,bird_size),pygame.SRCALPHA)
bird_angle = 0
bird_up_time = 30
bird_up_cnt = 0

pipes = []
pipe_spawn_cd = 60
pipe_spawn_time = 0
pipe_gap = 0.2*HEIGHT
pipe_img = pygame.image.load(path+'/assets/sprites/pipe.png')
pipe_img = pygame.transform.scale_by(pipe_img,(relative_scale,relative_scale))
pipe_spawn_x = WIDTH
pipe_speed = WIDTH/(2.5*60)

def rot_center(image : pygame.Surface, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image.copy(), angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def draw_screen():
    window.fill("black")
    window.blit(background_img,(0,0))

    for pipe_pos in pipes:
        window.blit(pipe_img,pipe_pos)

    window.blit(ground_img,(0,HEIGHT-ground_height))
    window.blit(rot_center(bird_img,bird_angle),bird_pos)


def update_pipe():
    global pipe_spawn_time,pipes
    pipe_spawn_time += 1
    if pipe_spawn_time >= pipe_spawn_cd:
        pipe_spawn_time = 0
        pipes.append(Vector2(pipe_spawn_x,randrange(0,HEIGHT-ground_height)))

def update_bird():
    global bird_img_id,bird_anim_cnt,bird_vely,bird_angle,bird_up_cnt

    bird_anim_cnt+=1
    if bird_anim_cnt >= bird_anim_delay:
        bird_img_id+=1
        bird_img_id%=4
        bird_anim_cnt -= bird_anim_delay
    bird_img.blit(bird_sprites,(0,0),(bird_img_id*bird_size,0,bird_size,bird_size))
    bird_vely += gravity
    bird_pos.y += bird_vely

    bird_up_cnt+=1
    if bird_up_cnt >= bird_up_time:
        bird_angle -= 8
        if bird_angle < -90:
            bird_angle = -90

def update():
    update_bird()
    update_pipe()

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    bird_pos.xy = (WIDTH/3 - bird_size/2,HEIGHT/2 - bird_size/2)
                    bird_vely = 0
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird_vely = -bird_jump_vel
                    bird_angle = 30
                    bird_up_cnt = 0
        update()
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
