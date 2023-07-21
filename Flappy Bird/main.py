from random import randint, randrange
import pygame,math,sys,time,os
from pygame import Vector2
pygame.init()
scale = 2
gravity = 0.3*scale
tile_size = 32*scale
ground_height = tile_size*3
bird_size = tile_size*2
relative_scale = bird_size//32

WIDTH,HEIGHT = relative_scale*144,relative_scale*256

window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

path = os.path.dirname(os.path.abspath(__file__))
background_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/background_day.png'),(WIDTH,HEIGHT))
ground_img = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/ground.png'),(WIDTH,ground_height))
instruction_img = pygame.transform.scale_by(pygame.image.load(path+'/assets/sprites/instruction.png'),(relative_scale,relative_scale))
get_ready_img = pygame.transform.scale_by(pygame.image.load(path+'/assets/sprites/get_ready.png'),(relative_scale,relative_scale))
game_title_img = pygame.transform.scale_by(pygame.image.load(path+'/assets/sprites/game_title.png'),(relative_scale,relative_scale))
play_button_img = pygame.transform.scale_by(pygame.image.load(path+'/assets/sprites/play_button.png'),(relative_scale,relative_scale))
play_button_rect = play_button_img.get_rect(center = (WIDTH/2,HEIGHT*2/3))
score_font = pygame.font.Font(path+'/assets/font/04B_19__.TTF',80)

flap_sfx = pygame.mixer.Sound(path+'/assets/sfx/flap.wav')
die_sfx = pygame.mixer.Sound(path+'/assets/sfx/die.wav')
score_up_sfx = pygame.mixer.Sound(path+'/assets/sfx/score_up.wav')

flash_surf = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
flash_surf.fill('white')
flash_speed = 35
flash_surf.set_alpha(0)
flash_val = -255

is_playing = False

bird_die = pygame.USEREVENT + 1
is_alive = True
bird_sprites = pygame.transform.scale(pygame.image.load(path+'/assets/sprites/bird.png'),(bird_size*4,bird_size))
bird_img_id = 0
bird_anim_delay = 5
bird_anim_cnt = 0
bird_pos = Vector2(WIDTH/3 - bird_size/2,HEIGHT/2 - bird_size/2)
bird_vely = 0.0
bird_jump_vel = 12
bird_img = pygame.Surface((bird_size,bird_size),pygame.SRCALPHA)
bird_hitbox = bird_img.get_rect(center = bird_pos).copy().inflate(-bird_size/2-15,-15-bird_size/2)
cur_bird_surf = pygame.Surface((0,0))
bird_angle = 0
bird_up_time = 30
bird_up_cnt = 0
bird_score = 0

pipes : list[list[pygame.Rect]]= []
pipe_spawn_cd = 80
pipe_spawn_time = 0
pipe_gap = 0.2*HEIGHT
pipe_img = pygame.image.load(path+'/assets/sprites/pipe.png')
pipe_img = pygame.transform.scale_by(pipe_img,(relative_scale,relative_scale))
pipe_spawn_x = WIDTH
pipe_speed = WIDTH/(2.5*60)
spawn_range = int(0.15*HEIGHT),int(HEIGHT-ground_height - 0.15*HEIGHT - pipe_gap)

def reset_game():
    global bird_pos,bird_vely,bird_angle,bird_score,bird_anim_cnt,is_alive,is_playing
    bird_pos.xy = (WIDTH/3 - bird_size/2,HEIGHT/2 - bird_size/2)
    bird_vely = 0
    bird_angle = 0
    bird_score = 0
    bird_anim_cnt = 0
    pipes.clear()
    is_alive = True
    is_playing = False

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
    if is_playing:
        for pipe_info in pipes:
            window.blit(pipe_img,pipe_info[0])
            window.blit(pygame.transform.flip(pipe_img,False,True),pipe_info[1])
        if not is_alive:
            window.blit(play_button_img,play_button_rect)
    else:
        window.blit(instruction_img,(WIDTH/2-instruction_img.get_width()/2,HEIGHT/2-instruction_img.get_height()/2))
        window.blit(
            get_ready_img,
            (
                WIDTH/2-get_ready_img.get_width()/2,
                HEIGHT/2-instruction_img.get_height()/2-get_ready_img.get_height()
            )
        )
        window.blit(
            game_title_img,
            (
                WIDTH/2-get_ready_img.get_width()/2,
                (HEIGHT/2-instruction_img.get_height()/2-get_ready_img.get_height())/2-game_title_img.get_height()/2
            )
        )
    window.blit(ground_img,(0,HEIGHT-ground_height))
    window.blit(cur_bird_surf,bird_pos)

    if is_playing:
        score_text = score_font.render(str(bird_score),False,"white","black")
        window.blit(score_text,(WIDTH/2-score_text.get_width()/2,0.1*HEIGHT))

    window.blit(flash_surf,(0,0))

def update_pipe():
    global pipe_spawn_time,pipes
    if is_alive:
        pipe_spawn_time += 1
        if pipe_spawn_time >= pipe_spawn_cd:
            pipe_spawn_time = 0
            top = randrange(*spawn_range)
            pipes.append(
                [
                    pipe_img.get_rect(bottom = top, left = pipe_spawn_x).copy(),
                    pipe_img.get_rect(top = top + pipe_gap, left = pipe_spawn_x).copy(),
                    pygame.Rect(pipe_spawn_x+pipe_img.get_width()/2,top,pipe_img.get_width()/2,pipe_gap)
                ]
            )
            if len(pipes) > 0 and pipes[0][0].right < 0:
                pipes.pop(0)
        for pipe_info in pipes:
            for rect in pipe_info:
                rect.right -= pipe_speed

def update_bird():
    global bird_img_id,bird_anim_cnt,bird_vely,bird_angle,bird_up_cnt,cur_bird_surf
    if is_playing:
        if is_alive:
            bird_anim_cnt+=1
            if bird_anim_cnt >= bird_anim_delay:
                bird_img_id+=1
                bird_img_id%=4
                bird_anim_cnt -= bird_anim_delay
        bird_vely += gravity
        bird_pos.y += bird_vely

        bird_img.blit(bird_sprites,(0,0),(bird_img_id*bird_size,0,bird_size,bird_size))
        bird_hitbox.center = bird_pos[0]+cur_bird_surf.get_width()/2,bird_pos[1]+cur_bird_surf.get_height()/2
        bird_up_cnt+=1
        if bird_up_cnt >= bird_up_time:
            bird_angle -= 8
            if bird_angle < -90:
                bird_angle = -90
                
        if bird_hitbox.top < 0:
            bird_hitbox.top = 0
            bird_vely = 0
        
        cur_bird_surf = rot_center(bird_img,bird_angle)
    else:
        bird_anim_cnt+=1
        if bird_anim_cnt >= bird_anim_delay:
            bird_img_id+=1
            bird_img_id%=4
            bird_anim_cnt -= bird_anim_delay
        bird_pos.y = 9*math.sin(time.time()*9)+HEIGHT/2-bird_size/2
        bird_img.blit(bird_sprites,(0,0),(bird_img_id*bird_size,0,bird_size,bird_size))
        cur_bird_surf = rot_center(bird_img,bird_angle)

def collision_check():
    global bird_vely,bird_score
    if is_alive:
        for pipe_info in pipes:
            for pipe in pipe_info[:2]:
                if bird_hitbox.colliderect(pipe):
                    pygame.event.post(pygame.event.Event(bird_die))
                    break
            if bird_hitbox.colliderect(pipe_info[2]):
                bird_score+=1
                pipe_info[2].bottom = 0
                score_up_sfx.play()

    if bird_hitbox.bottom > HEIGHT - ground_height:
        bird_pos.y = HEIGHT - ground_height - bird_hitbox.h
        bird_vely = 0
        if is_alive:
            pygame.event.post(pygame.event.Event(bird_die))

def update_flash():
    global flash_val
    if flash_val > -255:
        flash_val += flash_speed
        if flash_val > 255:
            flash_val = -255
        flash_surf.set_alpha(255-abs(flash_val))

def update():
    update_bird()
    update_flash()
    if is_playing:
        update_pipe()
        collision_check()


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == bird_die:
                flash_val += is_alive
                if is_alive:
                    die_sfx.play()
                is_alive = False
            elif is_alive and (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                is_playing = True
                bird_vely = -bird_jump_vel
                bird_angle = 30
                bird_up_cnt = 0
                flap_sfx.play()
            elif is_alive == False and (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) and play_button_rect.collidepoint(pygame.mouse.get_pos()):
                reset_game()
        update()
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
