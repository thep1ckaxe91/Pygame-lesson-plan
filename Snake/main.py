from random import *
import pygame,math,sys
from pygame.math import Vector2,clamp
from pygame import threads
pygame.init()
pygame.mixer.init()
WIDTH,HEIGHT = 1366,768
BGCOLOR = pygame.Color("black")
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

eat_sfx = pygame.mixer.Sound("assets/eat.wav")
die_sfx = pygame.mixer.Sound("assets/die.wav")


game_border_offset = 62
game_border_thickness = 2
game_border_rect = pygame.Rect(game_border_offset,game_border_offset,WIDTH-game_border_offset*2,HEIGHT-game_border_offset*2)
tile_size = 46
row_num = game_border_rect.height//tile_size
col_num = game_border_rect.width//tile_size

snake_die = pygame.USEREVENT + 1
snake_color = (100,100,200)
snake_body_init_pos = [
    Vector2(col_num//2*tile_size + game_border_offset,game_border_rect.h//2 + game_border_offset),
    Vector2(col_num//2*tile_size - tile_size + game_border_offset,game_border_rect.h//2 + game_border_offset),
    Vector2(col_num//2*tile_size - tile_size*2 + game_border_offset,game_border_rect.h//2 + game_border_offset),
]
snake_body_pos = [body.copy() for body in snake_body_init_pos]
direction = {
    "up"    : Vector2(0,-1),
    "down"  : Vector2(0,1),
    "left"  : Vector2(-1,0),
    "right" : Vector2(1,0),
    "none"  : Vector2(0,0)
}
snake_cur_dir = direction['none']
snake_next_dir = direction['none']
snake_move_cd = 60//5#frame
move_cd_cnt = 0

food_color = (255,0,0)
food_pos = Vector2(
    randrange(0,col_num)*tile_size + game_border_offset,
    randrange(0,row_num)*tile_size + game_border_offset,
)

def init_game():
    global snake_body_pos,snake_next_dir
    snake_next_dir = direction["none"]
    snake_body_pos = [body.copy() for body in snake_body_init_pos]

def draw_food():
    pygame.draw.rect(window,food_color,(food_pos.x,food_pos.y,tile_size,tile_size))

def spawn_food():
    global food_pos
    spawnable_pos = []
    for y in range(0,row_num):
        for x in range(0,col_num):
            checkpos = (int((x+0.5)*tile_size + game_border_offset), int((y+0.5)*tile_size + game_border_offset))
            if window.get_at(checkpos) == BGCOLOR:
                spawnable_pos.append(Vector2(x*tile_size+game_border_offset,y*tile_size+game_border_offset))
    food_pos = choice(spawnable_pos)
def food_manager():
    if snake_body_pos[0] == food_pos:
        eat_sfx.play()
        snake_body_pos.append(snake_body_pos[-1].copy())
        spawn_food()

def update_snake():
    global move_cd_cnt,snake_body_pos,snake_cur_dir
    if snake_next_dir != direction['none']:
        if move_cd_cnt >= snake_move_cd:
            snake_cur_dir = snake_next_dir
            for i in range(len(snake_body_pos)-1, 0, -1):
                snake_body_pos[i] = snake_body_pos[i-1].copy()
            snake_body_pos[0] += snake_cur_dir*tile_size

            if snake_body_pos[0].y < game_border_offset:
                snake_body_pos[0].y = (row_num-1)*tile_size + game_border_offset
            elif snake_body_pos[0].y >= game_border_offset + row_num*tile_size:
                snake_body_pos[0].y = game_border_offset
            elif snake_body_pos[0].x < game_border_offset:
                snake_body_pos[0].x = (col_num-1)*tile_size + game_border_offset
            elif snake_body_pos[0].x >= game_border_offset + col_num*tile_size:
                snake_body_pos[0].x = game_border_offset
            
            #check collide with self
            for i in range(1,len(snake_body_pos)):
                if snake_body_pos[0]==snake_body_pos[i]:
                    pygame.event.post(pygame.event.Event(snake_die))
                    break

            move_cd_cnt = 0
        move_cd_cnt += 1

def draw_snake():
    for i,body in enumerate(snake_body_pos):
        pygame.draw.rect(
            window,
            (clamp(int(body.x/game_border_rect.w*255),0,255),clamp(int(body.y/game_border_rect.h*255),0,255),200),
            (body.x + (i/len(snake_body_pos)*tile_size/4),body.y + (i/len(snake_body_pos)*tile_size/4),tile_size - (i/len(snake_body_pos)*tile_size/2),tile_size - (i/len(snake_body_pos)*tile_size/2))
        )

def update():
    update_snake()
    food_manager()

def draw_screen():
    window.fill(BGCOLOR)
    pygame.draw.rect(window,"white",game_border_rect,game_border_thickness)
    draw_snake()
    draw_food()
    print(snake_body_init_pos)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and snake_cur_dir!=direction['up']:
                snake_next_dir = direction["down"]
            if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and snake_cur_dir!=direction['left']:
                snake_next_dir = direction["right"]
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and snake_cur_dir!=direction['right'] and snake_cur_dir!=direction["none"]:
                snake_next_dir = direction["left"]
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and snake_cur_dir!=direction['down']:
                snake_next_dir = direction["up"]
        if event.type == snake_die:
            init_game()
            die_sfx.play()

    update()
    pygame.display.flip()
    clock.tick(60)

#'''